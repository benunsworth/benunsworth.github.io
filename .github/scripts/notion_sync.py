#!/usr/bin/env python3
"""
Notion-to-Jekyll Sync Script with Image Optimization
Issue #11: Notion-to-Jekyll Python Sync Script with Image Optimization

Queries Notion database for pages where `Publish State == 'Ready to Publish'`,
converts blocks to Jekyll Markdown, downloads and optimizes images with Pillow,
normalises Digital Garden metadata, writes the post file to `_posts/`,
and updates the Notion page state to `Published` with the live URL.
"""

import argparse
import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageOps

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

NOTION_API_VERSION = "2022-06-28"
NOTION_API_URL = "https://api.notion.com/v1"
SITE_URL = "https://benunsworth.co.uk"


# ---------------------------------------------------------------------------
# Notion API Client
# ---------------------------------------------------------------------------

class NotionClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
            "User-Agent": "BenUnsworthBlogPublisher/1.0",
        }

    def _request(self, endpoint: str, method: str = "GET", data: dict = None) -> dict:
        url = f"{NOTION_API_URL}/{endpoint.lstrip('/')}"
        encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=encoded_data, headers=self.headers, method=method)

        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                err_json = json.loads(error_body)
                err_msg = err_json.get("message", error_body)
            except Exception:
                err_msg = error_body
            raise RuntimeError(f"Notion API error (HTTP {e.code}) on {method} {endpoint}: {err_msg}")

    def query_ready_posts(self, database_id: str) -> list:
        """Fetch all pages in the database where Publish State == 'Ready to Publish'."""
        pages = []
        has_more = True
        start_cursor = None

        while has_more:
            payload = {
                "filter": {
                    "property": "Publish State",
                    "select": {
                        "equals": "Ready to Publish"
                    }
                }
            }
            if start_cursor:
                payload["start_cursor"] = start_cursor

            res = self._request(f"databases/{database_id}/query", method="POST", data=payload)
            pages.extend(res.get("results", []))
            has_more = res.get("has_more", False)
            start_cursor = res.get("next_cursor")

        return pages

    def get_page(self, page_id: str) -> dict:
        """Fetch single page metadata."""
        return self._request(f"pages/{page_id}", method="GET")

    def get_block_children(self, block_id: str) -> list:
        """Recursively fetch all children blocks for a given block/page."""
        blocks = []
        has_more = True
        start_cursor = None

        while has_more:
            endpoint = f"blocks/{block_id}/children?page_size=100"
            if start_cursor:
                endpoint += f"&start_cursor={start_cursor}"

            res = self._request(endpoint, method="GET")
            results = res.get("results", [])
            for block in results:
                if block.get("has_children") and block.get("type") not in ("child_page", "child_database"):
                    try:
                        block["children"] = self.get_block_children(block["id"])
                    except Exception as e:
                        print(f"Warning: failed to fetch children for block {block['id']}: {e}", file=sys.stderr)
                        block["children"] = []
                blocks.append(block)

            has_more = res.get("has_more", False)
            start_cursor = res.get("next_cursor")

        return blocks

    def update_page_to_published(self, page_id: str, post_url: str):
        """Update Notion page properties: set Publish State to Published and write Post URL."""
        payload = {
            "properties": {
                "Publish State": {
                    "select": {"name": "Published"}
                },
                "Post URL": {
                    "url": post_url
                }
            }
        }
        return self._request(f"pages/{page_id}", method="PATCH", data=payload)


# ---------------------------------------------------------------------------
# Formatting Helpers: Slugs, Tags, Dates, and Rich Text
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to a clean URL-friendly slug."""
    text = text.strip().lower()
    text = re.sub(r"['’]", "", text)  # remove apostrophes
    text = re.sub(r"[^a-z0-9]+", "-", text)  # replace non-alphanumeric with hyphens
    return text.strip("-") or "post"


def normalise_tag(tag: str) -> str:
    """Normalise a tag to lowercase hyphenated format."""
    tag = tag.strip().lower()
    tag = re.sub(r"['’]", "", tag)
    tag = re.sub(r"[\s_]+", "-", tag)
    tag = re.sub(r"[^a-z0-9\-]+", "", tag)
    return tag.strip("-")


def extract_plain_text(rich_text_array: list) -> str:
    """Extract concatenated plain text from a Notion rich_text list."""
    if not rich_text_array:
        return ""
    return "".join(t.get("plain_text", "") for t in rich_text_array)


def render_rich_text(rich_text_array: list) -> str:
    """Render a Notion rich_text array to Markdown."""
    if not rich_text_array:
        return ""

    out = []
    for item in rich_text_array:
        text = item.get("plain_text", "")
        if not text:
            continue

        annotations = item.get("annotations", {})
        href = item.get("href")

        # Preserve surrounding spaces outside markdown formatting
        leading_space = re.match(r"^(\s*)", text).group(1)
        trailing_space = re.search(r"(\s*)$", text).group(1)
        core = text[len(leading_space):len(text) - len(trailing_space)] if len(text) > (len(leading_space) + len(trailing_space)) else ""

        if not core:
            out.append(text)
            continue

        if annotations.get("code"):
            core = f"`{core}`"
        if annotations.get("bold"):
            core = f"**{core}**"
        if annotations.get("italic"):
            core = f"*{core}*"
        if annotations.get("strikethrough"):
            core = f"~~{core}~~"

        if href:
            core = f"[{core}]({href})"

        out.append(leading_space + core + trailing_space)

    return "".join(out)


# ---------------------------------------------------------------------------
# Image Handling & Pillow Optimization
# ---------------------------------------------------------------------------

def download_and_optimize_image(
    image_url: str,
    output_dir: Path,
    slug: str,
    index: int,
    max_width: int = 1600,
    quality: int = 83,
) -> tuple[str, str]:
    """
    Download image from URL, optimize with Pillow, save to output_dir,
    and return relative asset path and local file path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch image bytes
    req = urllib.request.Request(
        image_url,
        headers={"User-Agent": "BenUnsworthBlogPublisher/1.0"},
    )
    with urllib.request.urlopen(req) as resp:
        content_type = resp.headers.get("Content-Type", "")
        raw_bytes = resp.read()

    filename = f"{slug}-{index}.jpg"
    dest_path = output_dir / filename

    if PILLOW_AVAILABLE:
        try:
            img = Image.open(io.BytesIO(raw_bytes))
            # Fix mobile EXIF orientation
            img = ImageOps.exif_transpose(img)

            # Convert RGBA / CMYK / P to RGB for JPEG saving
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Resize if wider than max_width
            if img.width > max_width:
                proportional_height = int((max_width / img.width) * img.height)
                img = img.resize((max_width, proportional_height), Image.Resampling.LANCZOS)

            # Save optimized JPEG
            img.save(dest_path, "JPEG", quality=quality, optimize=True)
        except Exception as e:
            print(f"Warning: Pillow optimization failed ({e}), writing raw bytes", file=sys.stderr)
            with open(dest_path, "wb") as f:
                f.write(raw_bytes)
    else:
        with open(dest_path, "wb") as f:
            f.write(raw_bytes)

    # Determine Jekyll-relative path (e.g. /public/images/posts/2026/slug-1.jpg)
    rel_path = "/" + str(dest_path.as_posix()).split("/public/", 1)[-1]
    rel_path = f"/public/{rel_path.lstrip('/')}"
    return rel_path, str(dest_path)


# ---------------------------------------------------------------------------
# Block-to-Markdown Parser
# ---------------------------------------------------------------------------

class BlockParser:
    def __init__(self, post_year: str, post_slug: str, post_title: str):
        self.year = post_year
        self.slug = post_slug
        self.title = post_title
        self.images = []  # List of dicts: {"rel_path": ..., "alt": ...}
        self.image_counter = 1

    def parse_blocks(self, blocks: list, indent_level: int = 0) -> str:
        """Convert a list of Notion block dictionaries into Markdown text."""
        output = []
        numbered_list_idx = 1

        for idx, block in enumerate(blocks):
            btype = block.get("type")
            bdata = block.get(btype, {})

            # Reset numbered list counter if block is not numbered_list_item
            if btype != "numbered_list_item":
                numbered_list_idx = 1

            indent = "  " * indent_level

            if btype == "paragraph":
                text = render_rich_text(bdata.get("rich_text", []))
                output.append(f"{indent}{text}\n" if text else "\n")

            elif btype == "heading_1":
                # Notion H1 maps to Markdown ## to preserve Jekyll H1 title layout
                text = render_rich_text(bdata.get("rich_text", []))
                output.append(f"\n{indent}## {text}\n\n")

            elif btype == "heading_2":
                # Notion H2 maps to Markdown ###
                text = render_rich_text(bdata.get("rich_text", []))
                output.append(f"\n{indent}### {text}\n\n")

            elif btype == "heading_3":
                # Notion H3 maps to Markdown ####
                text = render_rich_text(bdata.get("rich_text", []))
                output.append(f"\n{indent}#### {text}\n\n")

            elif btype == "bulleted_list_item":
                text = render_rich_text(bdata.get("rich_text", []))
                output.append(f"{indent}- {text}\n")
                if block.get("children"):
                    output.append(self.parse_blocks(block["children"], indent_level + 1))

            elif btype == "numbered_list_item":
                text = render_rich_text(bdata.get("rich_text", []))
                output.append(f"{indent}{numbered_list_idx}. {text}\n")
                numbered_list_idx += 1
                if block.get("children"):
                    output.append(self.parse_blocks(block["children"], indent_level + 1))

            elif btype == "to_do":
                text = render_rich_text(bdata.get("rich_text", []))
                checked = bdata.get("checked", False)
                box = "[x]" if checked else "[ ]"
                output.append(f"{indent}- {box} {text}\n")
                if block.get("children"):
                    output.append(self.parse_blocks(block["children"], indent_level + 1))

            elif btype == "quote":
                text = render_rich_text(bdata.get("rich_text", []))
                output.append(f"\n{indent}> {text}\n\n")
                if block.get("children"):
                    output.append(self.parse_blocks(block["children"], indent_level + 1))

            elif btype == "callout":
                icon = bdata.get("icon", {})
                emoji = icon.get("emoji", "") if icon.get("type") == "emoji" else ""
                prefix = f"{emoji} " if emoji else ""
                text = render_rich_text(bdata.get("rich_text", []))
                callout_html = f'<aside class="callout">\n  <p>{prefix}{text}</p>\n</aside>\n\n'
                output.append(callout_html)

            elif btype == "code":
                text = extract_plain_text(bdata.get("rich_text", []))
                lang = bdata.get("language", "").strip().lower()
                if lang == "plain text":
                    lang = ""
                output.append(f"\n```{lang}\n{text}\n```\n\n")

            elif btype == "divider":
                output.append("\n---\n\n")

            elif btype == "bookmark":
                url = bdata.get("url", "")
                caption = extract_plain_text(bdata.get("caption", []))
                link_text = caption if caption else url
                output.append(f"\n[{link_text}]({url})\n\n")

            elif btype == "image":
                img_url = ""
                if bdata.get("type") == "file":
                    img_url = bdata.get("file", {}).get("url", "")
                elif bdata.get("type") == "external":
                    img_url = bdata.get("external", {}).get("url", "")

                if img_url:
                    caption = extract_plain_text(bdata.get("caption", []))
                    alt_text = caption if caption else self.title

                    target_dir = Path("public/images/posts") / self.year
                    try:
                        rel_path, _ = download_and_optimize_image(
                            img_url,
                            target_dir,
                            self.slug,
                            self.image_counter,
                        )
                        self.images.append({"rel_path": rel_path, "alt": alt_text})
                        self.image_counter += 1
                        output.append(f"\n![{alt_text}]({rel_path})\n\n")
                    except Exception as e:
                        print(f"Error downloading image: {e}", file=sys.stderr)

        # Clean multiple blank lines
        clean_text = "".join(output)
        clean_text = re.sub(r"\n{3,}", "\n\n", clean_text).strip() + "\n"
        return clean_text


# ---------------------------------------------------------------------------
# Front Matter Builder
# ---------------------------------------------------------------------------

def build_front_matter(properties: dict, fallback_slug: str, lead_image: dict = None) -> tuple[dict, str, str]:
    """
    Construct valid Jekyll front matter dictionary and extract post date and slug.
    Returns (front_matter_dict, post_date_str, post_slug_str).
    """
    # 1. Title
    title_items = properties.get("Title", {}).get("title", [])
    title = extract_plain_text(title_items).strip() or "Untitled"

    # 2. Slug
    slug_prop = extract_plain_text(properties.get("Slug", {}).get("rich_text", [])).strip()
    slug = slugify(slug_prop) if slug_prop else fallback_slug

    # 3. Date
    date_prop = properties.get("Date", {}).get("date")
    if date_prop and date_prop.get("start"):
        post_date = date_prop["start"][:10]  # format: YYYY-MM-DD
    else:
        post_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 4. Stream Type
    type_select = properties.get("Type", {}).get("select")
    raw_type = type_select.get("name", "note") if type_select else "note"
    allowed_types = {"weeknote", "note", "essay", "review", "reading"}
    post_type = raw_type if raw_type in allowed_types else "note"

    # 5. Garden Status
    status_select = properties.get("Status", {}).get("select")
    raw_status = status_select.get("name", "rough") if status_select else "rough"
    allowed_statuses = {"rough", "in-progress", "settled"}
    post_status = raw_status if raw_status in allowed_statuses else "rough"

    # 6. Tags
    tags_prop = properties.get("Tags", {}).get("multi_select", [])
    normalised_tags = []
    for tag_item in tags_prop:
        tname = normalise_tag(tag_item.get("name", ""))
        if tname and tname not in normalised_tags:
            normalised_tags.append(tname)

    # 7. Media (Reviews only)
    media_select = properties.get("Media", {}).get("select")
    media = media_select.get("name") if media_select else None

    # 8. Rating (Reviews only)
    rating_prop = properties.get("Rating", {})
    rating = None
    if rating_prop.get("type") == "select" and rating_prop.get("select"):
        rating = rating_prop["select"].get("name")
    elif rating_prop.get("type") == "number" and rating_prop.get("number") is not None:
        rating = str(rating_prop["number"])

    # 9. Summary
    summary_items = properties.get("Summary", {}).get("rich_text", [])
    summary = extract_plain_text(summary_items).strip()

    # Construct Front Matter
    fm = {
        "layout": "post",
        "title": title,
    }

    if normalised_tags:
        fm["tags"] = normalised_tags

    fm["type"] = post_type
    fm["status"] = post_status

    if media and (post_type == "review" or media in {"book", "podcast", "tv", "film", "game"}):
        fm["media"] = media

    if rating:
        # Validate rating increment
        try:
            r_float = float(rating)
            if 0.5 <= r_float <= 5.0 and (r_float * 2).is_integer():
                fm["rating"] = int(r_float) if r_float.is_integer() else r_float
        except ValueError:
            pass

    if lead_image:
        fm["image"] = lead_image["rel_path"]
        fm["image_alt"] = lead_image["alt"]

    if summary:
        fm["summary"] = summary

    # Only include explicit date in front matter if user overrode it
    if date_prop and date_prop.get("start"):
        fm["date"] = post_date

    return fm, post_date, slug


def format_front_matter_yaml(fm: dict) -> str:
    """Format dictionary into standard YAML front matter."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            tags_str = ", ".join(v)
            lines.append(f"{k}: [{tags_str}]")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        elif isinstance(v, str):
            # Escape strings if they contain quotes or special YAML characters
            if '"' in v:
                escaped = v.replace('"', '\\"')
                lines.append(f'{k}: "{escaped}"')
            elif any(c in v for c in (':', '#', '[', ']', '{', '}', '&', '*', '!', '|', '>', "'", '%', '@', '`')):
                lines.append(f'{k}: "{v}"')
            else:
                lines.append(f'{k}: "{v}"' if k in ("title", "summary", "image_alt") else f"{k}: {v}")
    lines.append("---\n\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Post Processor & Notion Synchronizer
# ---------------------------------------------------------------------------

def sync_notion_posts(
    token: str,
    database_id: str,
    dry_run: bool = False,
    target_page_id: str = None,
) -> list[str]:
    """Sync all ready posts from Notion to Jekyll repository."""
    client = NotionClient(token)

    if target_page_id:
        print(f"Fetching specific Notion page ID: {target_page_id}...")
        pages = [client.get_page(target_page_id)]
    else:
        print(f"Querying database {database_id} for 'Ready to Publish' posts...")
        pages = client.query_ready_posts(database_id)

    if not pages:
        print("No posts marked 'Ready to Publish' found. Exiting cleanly (code 0).")
        return []

    print(f"Found {len(pages)} post(s) ready to publish.")
    created_files = []

    for page in pages:
        page_id = page["id"]
        props = page.get("properties", {})

        title_items = props.get("Title", {}).get("title", [])
        title = extract_plain_text(title_items).strip() or "Untitled"
        initial_slug = slugify(title)

        # Temporary date estimate to set image folder
        now_year = datetime.now(timezone.utc).strftime("%Y")

        print(f"\nProcessing post: \"{title}\" (Notion ID: {page_id})")

        # 1. Fetch child blocks
        blocks = client.get_block_children(page_id)

        # 2. Convert blocks to Markdown and optimize images
        parser = BlockParser(post_year=now_year, post_slug=initial_slug, post_title=title)
        body_markdown = parser.parse_blocks(blocks)

        lead_image = parser.images[0] if parser.images else None

        # 3. Build Front Matter
        fm, post_date, final_slug = build_front_matter(props, initial_slug, lead_image)
        post_year, post_month, post_day = post_date.split("-")

        # Re-check year if user overrode Date
        if post_year != now_year and parser.images:
            # Reorganize image directories if necessary
            pass

        # 4. Construct file content & path
        post_filename = f"{post_date}-{final_slug}.md"
        post_file_path = Path("_posts") / post_filename

        front_matter_yaml = format_front_matter_yaml(fm)
        full_content = front_matter_yaml + body_markdown

        # Calculate exact live URL: https://benunsworth.co.uk/YYYY/MM/DD/slug/
        live_post_url = f"{SITE_URL}/{post_year}/{post_month}/{post_day}/{final_slug}/"

        print(f"  Target File: {post_file_path}")
        print(f"  Live URL:    {live_post_url}")
        print(f"  Type:        {fm.get('type')}")
        print(f"  Status:      {fm.get('status')}")
        if fm.get("tags"):
            print(f"  Tags:        {fm.get('tags')}")
        if parser.images:
            print(f"  Images:      {len(parser.images)} image(s) optimized")

        if dry_run:
            print(f"  [DRY-RUN] Would write {len(full_content)} bytes to {post_file_path}")
            print(f"  [DRY-RUN] Would update Notion page {page_id} to Published with URL {live_post_url}")
        else:
            # Write post file
            post_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(post_file_path, "w", encoding="utf-8") as f:
                f.write(full_content)
            print(f"  [✓] Successfully wrote {post_file_path}")

            # Update Notion page
            try:
                client.update_page_to_published(page_id, live_post_url)
                print(f"  [✓] Updated Notion page status to 'Published'")
            except Exception as e:
                print(f"  [!] Failed to update Notion page {page_id}: {e}", file=sys.stderr)

        created_files.append(str(post_file_path))

    return created_files


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Notion-to-Jekyll Sync Script with Image Optimization"
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("NOTION_TOKEN"),
        help="Notion internal integration token (default: $NOTION_TOKEN)",
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("NOTION_DATABASE_ID"),
        help="Notion database ID (default: $NOTION_DATABASE_ID)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and validate without writing post files or updating Notion",
    )
    parser.add_argument(
        "--page-id",
        help="Sync only a specific Notion page ID (for testing/debugging)",
    )

    args = parser.parse_args()

    if not args.token:
        print("Error: Notion token is required via --token or NOTION_TOKEN env var.", file=sys.stderr)
        sys.exit(1)
    if not args.database_id and not args.page_id:
        print("Error: Database ID is required via --database-id or NOTION_DATABASE_ID env var.", file=sys.stderr)
        sys.exit(1)

    try:
        created = sync_notion_posts(
            token=args.token,
            database_id=args.database_id,
            dry_run=args.dry_run,
            target_page_id=args.page_id,
        )
        print(f"\nDone! Processed {len(created)} post(s).")
    except Exception as e:
        print(f"\nSync failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
