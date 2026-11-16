#!/usr/bin/env python3
"""
Bootstrap Notion Database for Ben Unsworth's Digital Garden
Issue #10: Notion Database Schema & Integration Setup

Creates a dedicated Notion database under a specified parent page with all 11
properties required by the Digital Garden ontology.

Uses Python 3 standard library only (no external dependencies).
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

NOTION_API_VERSION = "2022-06-28"
NOTION_API_URL = "https://api.notion.com/v1"


def extract_uuid(input_str: str) -> str:
    """Extract standard formatted UUID from a Notion URL, raw string, or hyphenated ID."""
    cleaned = input_str.strip()
    cleaned = re.sub(r"[?#].*$", "", cleaned)
    cleaned = cleaned.rstrip("/").split("/")[-1]

    # Standard UUID with hyphens: 8-4-4-4-12
    uuid_match = re.search(
        r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        cleaned,
    )
    if uuid_match:
        return uuid_match.group(1).lower()

    # In Notion URLs, the 32-char hex ID is usually at the very end of the slug
    end_match = re.search(r"([0-9a-fA-F]{32})$", cleaned)
    if end_match:
        raw = end_match.group(1).lower()
        return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"

    # Anywhere preceded by non-hex char or start of string
    match = re.search(r"(?:^|[^0-9a-fA-F])([0-9a-fA-F]{32})(?:[^0-9a-fA-F]|$)", cleaned)
    if match:
        raw = match.group(1).lower()
        return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"

    return cleaned


def create_database(token: str, parent_page_id: str, title: str = "Ben Unsworth Blog") -> dict:
    """Create the Notion database via the Notion REST API."""
    formatted_parent_id = extract_uuid(parent_page_id)

    payload = {
        "parent": {
            "type": "page_id",
            "page_id": formatted_parent_id,
        },
        "title": [
            {
                "type": "text",
                "text": {"content": title},
            }
        ],
        "properties": {
            "Title": {"title": {}},
            "Publish State": {
                "select": {
                    "options": [
                        {"name": "Draft", "color": "gray"},
                        {"name": "Ready to Publish", "color": "green"},
                        {"name": "Published", "color": "blue"},
                    ]
                }
            },
            "Type": {
                "select": {
                    "options": [
                        {"name": "note", "color": "gray"},
                        {"name": "weeknote", "color": "orange"},
                        {"name": "essay", "color": "purple"},
                        {"name": "review", "color": "blue"},
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "rough", "color": "yellow"},
                        {"name": "in-progress", "color": "orange"},
                        {"name": "settled", "color": "green"},
                    ]
                }
            },
            "Tags": {
                "multi_select": {
                    "options": [
                        {"name": "weeknotes", "color": "orange"},
                        {"name": "local-government", "color": "blue"},
                        {"name": "ai", "color": "purple"},
                        {"name": "service-design", "color": "green"},
                        {"name": "open-working", "color": "pink"},
                        {"name": "leadership", "color": "red"},
                        {"name": "technology", "color": "gray"},
                    ]
                }
            },
            "Media": {
                "select": {
                    "options": [
                        {"name": "book", "color": "brown"},
                        {"name": "podcast", "color": "purple"},
                        {"name": "tv", "color": "blue"},
                        {"name": "film", "color": "red"},
                        {"name": "game", "color": "green"},
                    ]
                }
            },
            "Rating": {
                "select": {
                    "options": [
                        {"name": "0.5", "color": "gray"},
                        {"name": "1", "color": "gray"},
                        {"name": "1.5", "color": "yellow"},
                        {"name": "2", "color": "yellow"},
                        {"name": "2.5", "color": "orange"},
                        {"name": "3", "color": "orange"},
                        {"name": "3.5", "color": "green"},
                        {"name": "4", "color": "green"},
                        {"name": "4.5", "color": "blue"},
                        {"name": "5", "color": "purple"},
                    ]
                }
            },
            "Summary": {"rich_text": {}},
            "Date": {"date": {}},
            "Slug": {"rich_text": {}},
            "Post URL": {"url": {}},
        },
    }

    req = urllib.request.Request(
        f"{NOTION_API_URL}/databases",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
            "User-Agent": "BenUnsworthBlogPublisher/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(error_body)
            err_msg = err_json.get("message", error_body)
        except Exception:
            err_msg = error_body
        raise RuntimeError(f"Notion API error (HTTP {e.code}): {err_msg}")


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap Notion Database for Ben Unsworth's Digital Garden"
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("NOTION_TOKEN"),
        help="Notion internal integration token (default: $NOTION_TOKEN)",
    )
    parser.add_argument(
        "--parent-page",
        required=True,
        help="Notion parent page ID or URL where the database will be created",
    )
    parser.add_argument(
        "--title",
        default="Ben Unsworth Blog",
        help="Database title (default: 'Ben Unsworth Blog')",
    )

    args = parser.parse_args()

    if not args.token:
        print("Error: Notion token is required via --token or NOTION_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to Notion API...")
    print(f"Parent Page ID/URL: {args.parent_page}")
    print(f"Database Title: {args.title}")

    try:
        result = create_database(args.token, args.parent_page, args.title)
        db_id = result.get("id")
        db_url = result.get("url")
        print("\n" + "=" * 60)
        print("SUCCESS! Notion database created successfully.")
        print(f"Database ID:  {db_id}")
        print(f"Database URL: {db_url}")
        print("=" * 60)
        print("\nNext steps:")
        print(f"1. Save this Database ID:")
        print(f"   NOTION_DATABASE_ID={db_id}")
        print("2. Set the GitHub Repository Secret:")
        print(f"   gh secret set NOTION_DATABASE_ID -R benunsworth/benunsworth.github.io -b \"{db_id}\"")
        print(f"   gh secret set NOTION_TOKEN -R benunsworth/benunsworth.github.io -b \"<YOUR_NOTION_TOKEN>\"")
        print("3. Run verification:")
        print(f"   python3 .github/scripts/verify_notion_setup.py --token \"...\" --database-id \"{db_id}\"")
    except Exception as e:
        print(f"\nFailed to create database: {e}", file=sys.stderr)
        print("\nTroubleshooting tips:", file=sys.stderr)
        print("1. Ensure your integration token has 'Insert content' capabilities.", file=sys.stderr)
        print("2. Verify that you have connected the integration to the parent page in Notion:", file=sys.stderr)
        print("   In Notion: Open parent page -> click '...' (top-right) -> Connections -> add your integration.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
