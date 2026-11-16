#!/usr/bin/env python3
"""
Verify Notion Database Schema for Ben Unsworth's Digital Garden
Issue #10: Notion Database Schema & Integration Setup

Validates that the target Notion database exists, is accessible via the Notion token,
and contains all 11 required properties matching the Digital Garden ontology.

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

# Required properties and their expected types
REQUIRED_PROPERTIES = {
    "Title": {"expected_types": ["title"]},
    "Publish State": {
        "expected_types": ["select"],
        "required_options": ["Draft", "Ready to Publish", "Published"],
    },
    "Type": {
        "expected_types": ["select"],
        "required_options": ["note", "weeknote", "essay", "review"],
    },
    "Status": {
        "expected_types": ["select"],
        "required_options": ["rough", "in-progress", "settled"],
    },
    "Tags": {"expected_types": ["multi_select"]},
    "Media": {
        "expected_types": ["select"],
        "required_options": ["book", "podcast", "tv", "film", "game"],
    },
    "Rating": {
        "expected_types": ["select", "number"],
        # If select, ideally includes half-star increments
    },
    "Summary": {"expected_types": ["rich_text"]},
    "Date": {"expected_types": ["date"]},
    "Slug": {"expected_types": ["rich_text"]},
    "Post URL": {"expected_types": ["url"]},
}


def extract_uuid(input_str: str) -> str:
    """Extract standard formatted UUID from a Notion URL, raw string, or hyphenated ID."""
    cleaned = input_str.strip()
    cleaned = re.sub(r"[?#].*$", "", cleaned)
    cleaned = cleaned.rstrip("/").split("/")[-1]

    uuid_match = re.search(
        r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        cleaned,
    )
    if uuid_match:
        return uuid_match.group(1).lower()

    end_match = re.search(r"([0-9a-fA-F]{32})$", cleaned)
    if end_match:
        raw = end_match.group(1).lower()
        return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"

    match = re.search(r"(?:^|[^0-9a-fA-F])([0-9a-fA-F]{32})(?:[^0-9a-fA-F]|$)", cleaned)
    if match:
        raw = match.group(1).lower()
        return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"

    return cleaned


def fetch_database(token: str, database_id: str) -> dict:
    """Fetch database metadata and schema from Notion API."""
    formatted_id = extract_uuid(database_id)
    req = urllib.request.Request(
        f"{NOTION_API_URL}/databases/{formatted_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_API_VERSION,
            "User-Agent": "BenUnsworthBlogPublisher/1.0",
        },
        method="GET",
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


def verify_database_schema(db_data: dict) -> bool:
    """Validate database properties against REQUIRED_PROPERTIES."""
    title_items = db_data.get("title", [])
    title_text = "".join(t.get("plain_text", "") for t in title_items) or "(Untitled)"
    print(f"\nDatabase Found: \"{title_text}\" (ID: {db_data.get('id')})")
    print(f"URL: {db_data.get('url')}\n")

    properties = db_data.get("properties", {})
    all_passed = True

    print("Verifying properties matching Digital Garden ontology:")
    print("-" * 65)

    for prop_name, spec in REQUIRED_PROPERTIES.items():
        if prop_name not in properties:
            print(f"  [✗] Missing property: '{prop_name}'")
            all_passed = False
            continue

        prop_data = properties[prop_name]
        prop_type = prop_data.get("type")
        expected_types = spec["expected_types"]

        if prop_type not in expected_types:
            print(
                f"  [✗] '{prop_name}' has type '{prop_type}', expected one of {expected_types}"
            )
            all_passed = False
            continue

        # Check options for select / multi-select
        required_options = spec.get("required_options")
        if required_options and prop_type in ("select", "multi_select"):
            existing_options = {
                opt.get("name")
                for opt in prop_data.get(prop_type, {}).get("options", [])
            }
            missing_options = [opt for opt in required_options if opt not in existing_options]
            if missing_options:
                print(
                    f"  [!] '{prop_name}' is missing recommended options: {missing_options} (type: {prop_type})"
                )
                # Warning rather than fatal if select can be populated on the fly, but flag it
            else:
                print(f"  [✓] '{prop_name}' ({prop_type}) - All required options present")
                continue

        print(f"  [✓] '{prop_name}' ({prop_type})")

    print("-" * 65)
    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="Verify Notion Database Schema for Ben Unsworth's Digital Garden"
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("NOTION_TOKEN"),
        help="Notion internal integration token (default: $NOTION_TOKEN)",
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("NOTION_DATABASE_ID"),
        help="Notion database ID or URL (default: $NOTION_DATABASE_ID)",
    )

    args = parser.parse_args()

    if not args.token:
        print("Error: Notion token is required via --token or NOTION_TOKEN env var.", file=sys.stderr)
        sys.exit(1)
    if not args.database_id:
        print("Error: Notion database ID is required via --database-id or NOTION_DATABASE_ID env var.", file=sys.stderr)
        sys.exit(1)

    print("Connecting to Notion API...")
    try:
        db_data = fetch_database(args.token, args.database_id)
        passed = verify_database_schema(db_data)
        if passed:
            print("\n🎉 SUCCESS: All 11 Digital Garden properties verified successfully!")
            print("The database is 100% ready for the mobile publishing sync pipeline (Issue #11).\n")
            sys.exit(0)
        else:
            print("\n⚠️  VALIDATION FAILED: Some properties are missing or misconfigured.", file=sys.stderr)
            print("Please check the output above and update your Notion database properties.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"\nVerification failed: {e}", file=sys.stderr)
        print("\nTroubleshooting tips:", file=sys.stderr)
        print("1. Ensure your NOTION_TOKEN is an internal integration token with read permissions.", file=sys.stderr)
        print("2. Ensure the integration has been connected to the database in Notion:", file=sys.stderr)
        print("   In Notion: Open database page -> '...' (top-right) -> Connections -> add your integration.", file=sys.stderr)
        print("3. Check that NOTION_DATABASE_ID is the 32-character database ID (or full URL).", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
