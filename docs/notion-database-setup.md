# Notion Database Schema & Integration Setup

This guide documents the Notion database schema and integration setup for the mobile publishing pipeline of [benunsworth.co.uk](https://benunsworth.co.uk).

It enables zero-maintenance, frictionless drafting on iPhone, iPad, or desktop, supporting the site's complete **Working in the Open** Digital Garden ontology.

---

## 1. Digital Garden Database Schema

The database properties match the site's canonical front matter schema (`AGENTS.md`):

| Property Name | Notion Property Type | Options / Values | Front Matter Mapping | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Title** | `title` | *(Post title)* | `title: "..."` | Main heading of the post |
| **Publish State** | `select` | `Draft`<br>`Ready to Publish`<br>`Published` | *(Workflow trigger)* | Sync pipeline only processes items marked `Ready to Publish`, then flips them to `Published`. |
| **Type** | `select` | `note` (default)<br>`weeknote`<br>`essay`<br>`review` | `type: ...` | Digital Garden stream type. Blank defaults to `note`. |
| **Status** | `select` | `rough`<br>`in-progress`<br>`settled` | `status: ...` | Garden stage rendered with optical vector glyphs (dashed, half, solid). |
| **Tags** | `multi_select` | `weeknotes`, `local-government`, `ai`, `service-design`, `open-working`, etc. | `tags: [...]` | Categorisation tags. Automatically normalised to lowercase hyphenated format. |
| **Media** | `select` | `book`, `podcast`, `tv`, `film`, `game` | `media: ...` | Optional media category (used when `Type` is `review`). |
| **Rating** | `select` | `0.5`, `1`, `1.5`, `2`, `2.5`, `3`, `3.5`, `4`, `4.5`, `5` | `rating: ...` | Single-tap review rating. Rendered as accessible SVG stars. |
| **Summary** | `rich_text` | *(Plain text)* | `summary: "..."` | One-sentence summary for card previews and SEO. |
| **Date** | `date` | *(YYYY-MM-DD)* | `date: YYYY-MM-DD` | Optional plant date override. If empty, defaults to publish date. |
| **Slug** | `rich_text` | *(Plain text)* | Filename slug | Optional custom URL slug. If empty, automatically derived from title. |
| **Post URL** | `url` | *(URL)* | *(Read-only)* | Populated automatically by the sync script with the live URL upon publishing. |

---

## 2. Step-by-Step Setup

### Step 1: Create an Internal Notion Integration
1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) in your browser.
2. Click **+ New integration**.
3. Name it **Garden Publisher** (or your preferred name).
4. Select the Notion workspace where your blog posts will live.
5. Under **Capabilities**, ensure **Read content**, **Update content**, and **Insert content** are checked.
6. Click **Save** / **Submit**, then copy the **Internal Integration Secret** (`secret_...` or `ntn_...`).

---

### Step 2: Create the Database

#### Option A: Automated Provisioning (Recommended)
You can let our Python script create the database with all 11 properties, colors, and options automatically:
1. In Notion, create a new blank page (e.g. titled "Blog" or "Digital Garden").
2. In the top-right menu (`...`) of the page, choose **Connections** > **Connect to** > select **Garden Publisher**.
3. Copy the URL or ID of the parent page from your browser address bar.
4. Run the setup script:
   ```bash
   python3 .github/scripts/setup_notion_database.py \
     --token "YOUR_NOTION_TOKEN" \
     --parent-page "https://www.notion.so/workspace/Page-Title-1234567890abcdef"
   ```
5. The script will output your newly created `NOTION_DATABASE_ID`.

#### Option B: Manual Creation in Notion
1. In Notion, click **+ Add a page** and select **Table** (New database).
2. Title it **Ben Unsworth Blog**.
3. Add each of the 11 properties listed in the table in [Section 1](#1-digital-garden-database-schema) with the exact names and types.
4. In the top-right menu (`...`) of the database, go to **Connections** > **Connect to** > select **Garden Publisher**.
5. Copy the 32-character database ID from the database URL:
   `https://www.notion.so/{workspace_name}/{database_id}?v=...`

---

### Step 3: Configure GitHub Repository Secrets

Configure two secrets in the GitHub repository:
- `NOTION_TOKEN`: Your internal integration secret from Step 1.
- `NOTION_DATABASE_ID`: The 32-character database ID from Step 2.

#### Via GitHub Web Interface:
1. Navigate to **Settings** > **Secrets and variables** > **Actions** in the repository.
2. Click **New repository secret**.
3. Add `NOTION_TOKEN`.
4. Add `NOTION_DATABASE_ID`.

#### Via GitHub CLI (`gh`):
```bash
gh secret set NOTION_TOKEN -R benunsworth/benunsworth.github.io -b "secret_..."
gh secret set NOTION_DATABASE_ID -R benunsworth/benunsworth.github.io -b "12345678-1234-1234-1234-123456789abc"
```

---

### Step 4: Verify the Setup

Run the zero-dependency verification script to confirm everything is connected and all 11 properties are valid:

```bash
python3 .github/scripts/verify_notion_setup.py \
  --token "$NOTION_TOKEN" \
  --database-id "$NOTION_DATABASE_ID"
```

Expected output:
```text
Database Found: "Ben Unsworth Blog" (ID: ...)
URL: https://www.notion.com/...

Verifying properties matching Digital Garden ontology:
-----------------------------------------------------------------
  [✓] 'Title' (title)
  [✓] 'Publish State' (select) - All required options present
  [✓] 'Type' (select) - All required options present
  [✓] 'Status' (select) - All required options present
  [✓] 'Tags' (multi_select)
  [✓] 'Media' (select) - All required options present
  [✓] 'Rating' (select)
  [✓] 'Summary' (rich_text)
  [✓] 'Date' (date)
  [✓] 'Slug' (rich_text)
  [✓] 'Post URL' (url)
-----------------------------------------------------------------

🎉 SUCCESS: All 11 Digital Garden properties verified successfully!
The database is 100% ready for the mobile publishing sync pipeline.
```

---

## 3. Mobile Drafting Tips (iPhone & iPad)

- **Create a "Drafts" View:** Set a Table or List view filtered to `Publish State` is `Draft`.
- **Create an "Add Post" Template:** In Notion database settings, create a template with `Type: note` and `Status: rough` pre-filled.
- **Photos & Images:** Drop photos directly into the Notion page body from your iPhone camera roll. Add an accessible caption in Notion (click image -> Caption); the sync script will download, resize, and convert it into an accessible `![alt](/public/images/posts/...)` markdown image.
- **Ready to Publish:** When you are ready to ship, simply switch `Publish State` to `Ready to Publish`.

---

## 4. Next Step: One-Tap Mobile Publishing

Once your Notion database and secrets are configured, follow the [**One-Tap iOS Shortcut & Mobile Setup Guide**](notion-mobile-publishing-setup.md) to set up single-tap publishing from your iPhone Home Screen, Control Center, or Action Button.
