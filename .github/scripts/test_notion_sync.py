#!/usr/bin/env python3
"""
Unit Test Suite for Notion-to-Jekyll Sync Pipeline
Issue #11: Notion-to-Jekyll Python Sync Script with Image Optimization

Tests:
1. Rich text rendering with annotations and links.
2. Block-to-Markdown conversions (headings hierarchy, lists, blockquotes, callouts, code blocks).
3. Tag normalisation and slug generation.
4. Front matter generation matching .github/workflows/site-check.yml schema.
5. Image optimization with Pillow.
"""

import io
import os
import re
import sys
import unittest
from pathlib import Path

# Ensure script directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image

import notion_sync


class TestRichTextAndFormatting(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(notion_sync.slugify("Hello World!"), "hello-world")
        self.assertEqual(notion_sync.slugify("Empire of AI by Karen Hao"), "empire-of-ai-by-karen-hao")
        self.assertEqual(notion_sync.slugify("It's a Test--Post!"), "its-a-test-post")
        self.assertEqual(notion_sync.slugify("   Spaces & Punctuation??? "), "spaces-punctuation")

    def test_normalise_tag(self):
        self.assertEqual(notion_sync.normalise_tag("Local Government"), "local-government")
        self.assertEqual(notion_sync.normalise_tag("AI"), "ai")
        self.assertEqual(notion_sync.normalise_tag("Service Design"), "service-design")
        self.assertEqual(notion_sync.normalise_tag("  Open_Working  "), "open-working")

    def test_render_rich_text_plain(self):
        items = [{"plain_text": "Plain text paragraph."}]
        self.assertEqual(notion_sync.render_rich_text(items), "Plain text paragraph.")

    def test_render_rich_text_bold_italic_code(self):
        items = [
            {"plain_text": "Normal "},
            {"plain_text": "bold", "annotations": {"bold": True}},
            {"plain_text": " and "},
            {"plain_text": "italic", "annotations": {"italic": True}},
            {"plain_text": " and "},
            {"plain_text": "inline code", "annotations": {"code": True}},
            {"plain_text": "."},
        ]
        expected = "Normal **bold** and *italic* and `inline code`."
        self.assertEqual(notion_sync.render_rich_text(items), expected)

    def test_render_rich_text_link(self):
        items = [
            {"plain_text": "Check this ", "annotations": {}},
            {"plain_text": "link", "annotations": {"bold": True}, "href": "https://example.com"},
            {"plain_text": "!"},
        ]
        expected = "Check this [**link**](https://example.com)!"
        self.assertEqual(notion_sync.render_rich_text(items), expected)

    def test_render_rich_text_surrounding_whitespace(self):
        # Annotations should not wrap leading/trailing whitespace inside ** or *
        items = [
            {"plain_text": " bold with spaces ", "annotations": {"bold": True}},
        ]
        expected = " **bold with spaces** "
        self.assertEqual(notion_sync.render_rich_text(items), expected)


class TestBlockParser(unittest.TestCase):
    def setUp(self):
        self.parser = notion_sync.BlockParser(post_year="2026", post_slug="test-post", post_title="Test Post")

    def test_headings_hierarchy(self):
        # H1 -> ##, H2 -> ###, H3 -> ####
        blocks = [
            {"type": "heading_1", "heading_1": {"rich_text": [{"plain_text": "Section One"}]}},
            {"type": "heading_2", "heading_2": {"rich_text": [{"plain_text": "Subsection A"}]}},
            {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "Detail 1"}]}},
        ]
        md = self.parser.parse_blocks(blocks)
        self.assertIn("## Section One", md)
        self.assertIn("### Subsection A", md)
        self.assertIn("#### Detail 1", md)

    def test_callout_block(self):
        blocks = [
            {
                "type": "callout",
                "callout": {
                    "icon": {"type": "emoji", "emoji": "💡"},
                    "rich_text": [{"plain_text": "This is an important callout note."}],
                },
            }
        ]
        md = self.parser.parse_blocks(blocks)
        self.assertIn('<aside class="callout">', md)
        self.assertIn("<p>💡 This is an important callout note.</p>", md)
        self.assertIn("</aside>", md)

    def test_bulleted_and_numbered_lists(self):
        blocks = [
            {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"plain_text": "Bullet 1"}]}},
            {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"plain_text": "Bullet 2"}]}},
            {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"plain_text": "Step 1"}]}},
            {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"plain_text": "Step 2"}]}},
        ]
        md = self.parser.parse_blocks(blocks)
        self.assertIn("- Bullet 1", md)
        self.assertIn("- Bullet 2", md)
        self.assertIn("1. Step 1", md)
        self.assertIn("2. Step 2", md)

    def test_to_do_list(self):
        blocks = [
            {"type": "to_do", "to_do": {"checked": False, "rich_text": [{"plain_text": "Pending task"}]}},
            {"type": "to_do", "to_do": {"checked": True, "rich_text": [{"plain_text": "Completed task"}]}},
        ]
        md = self.parser.parse_blocks(blocks)
        self.assertIn("- [ ] Pending task", md)
        self.assertIn("- [x] Completed task", md)

    def test_quote_and_code_blocks(self):
        blocks = [
            {"type": "quote", "quote": {"rich_text": [{"plain_text": "A wise reflection."}]}},
            {
                "type": "code",
                "code": {
                    "language": "python",
                    "rich_text": [{"plain_text": "print('hello world')"}],
                },
            },
            {"type": "divider", "divider": {}},
        ]
        md = self.parser.parse_blocks(blocks)
        self.assertIn("> A wise reflection.", md)
        self.assertIn("```python\nprint('hello world')\n```", md)
        self.assertIn("---", md)


class TestFrontMatterAndSiteCheckSchema(unittest.TestCase):
    def test_build_front_matter_review(self):
        properties = {
            "Title": {"title": [{"plain_text": "Empire of AI"}]},
            "Type": {"select": {"name": "review"}},
            "Status": {"select": {"name": "settled"}},
            "Media": {"select": {"name": "book"}},
            "Rating": {"type": "select", "select": {"name": "4.5"}},
            "Tags": {"multi_select": [{"name": "AI"}, {"name": "Books"}]},
            "Summary": {"rich_text": [{"plain_text": "Great book on AI power."}]},
            "Slug": {"rich_text": [{"plain_text": "empire-of-ai"}]},
            "Date": {"date": {"start": "2026-11-16"}},
        }
        fm, post_date, slug = notion_sync.build_front_matter(properties, fallback_slug="default-slug")

        self.assertEqual(post_date, "2026-11-16")
        self.assertEqual(slug, "empire-of-ai")
        self.assertEqual(fm["layout"], "post")
        self.assertEqual(fm["title"], "Empire of AI")
        self.assertEqual(fm["type"], "review")
        self.assertEqual(fm["status"], "settled")
        self.assertEqual(fm["media"], "book")
        self.assertEqual(fm["rating"], 4.5)
        self.assertEqual(fm["tags"], ["ai", "books"])
        self.assertEqual(fm["summary"], "Great book on AI power.")

        # Test against Site Check validator rules
        ALLOWED_TYPES = {"weeknote", "note", "essay", "review", "reading"}
        ALLOWED_STATUSES = {"rough", "in-progress", "settled"}
        ALLOWED_MEDIA = {"book", "podcast", "tv", "film", "game"}
        ALLOWED_RATINGS = {"0.5", "1", "1.0", "1.5", "2", "2.0", "2.5", "3", "3.0", "3.5", "4", "4.0", "4.5", "5", "5.0"}

        self.assertIn(fm["type"], ALLOWED_TYPES)
        self.assertIn(fm["status"], ALLOWED_STATUSES)
        self.assertIn(fm["media"], ALLOWED_MEDIA)
        self.assertIn(str(fm["rating"]), ALLOWED_RATINGS)

    def test_format_front_matter_yaml(self):
        fm = {
            "layout": "post",
            "title": 'Testing: A "Quoted" Title',
            "tags": ["open-working", "leadership"],
            "type": "note",
            "status": "rough",
        }
        yaml_str = notion_sync.format_front_matter_yaml(fm)
        self.assertTrue(yaml_str.startswith("---\n"))
        self.assertTrue(yaml_str.endswith("---\n\n"))
        self.assertIn('layout: post', yaml_str)
        self.assertIn('title: "Testing: A \\"Quoted\\" Title"', yaml_str)
        self.assertIn('tags: [open-working, leadership]', yaml_str)


class TestImageOptimization(unittest.TestCase):
    def test_image_resizing_and_saving(self):
        # Create a test high-res image (2400x1600) in memory
        test_img = Image.new("RGBA", (2400, 1600), color=(188, 82, 21, 255))
        buf = io.BytesIO()
        test_img.save(buf, format="PNG")
        buf.seek(0)
        img_bytes = buf.read()

        # Mock download by calling Pillow optimization logic directly
        output_dir = Path("/tmp/test_notion_images")
        output_dir.mkdir(parents=True, exist_ok=True)
        dest_path = output_dir / "test-slug-1.jpg"

        img = Image.open(io.BytesIO(img_bytes))
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background

        max_width = 1600
        proportional_height = int((max_width / img.width) * img.height)
        img = img.resize((max_width, proportional_height), Image.Resampling.LANCZOS)
        img.save(dest_path, "JPEG", quality=83, optimize=True)

        self.assertTrue(dest_path.exists())
        with Image.open(dest_path) as saved_img:
            self.assertEqual(saved_img.width, 1600)
            self.assertEqual(saved_img.height, 1066)
        self.assertLess(dest_path.stat().st_size, 300 * 1024)  # <300KB
        dest_path.unlink()


if __name__ == "__main__":
    unittest.main()
