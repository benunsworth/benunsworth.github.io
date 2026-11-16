# One-Tap iOS Shortcut & Mobile Publishing Setup

This guide walks you through setting up single-tap mobile publishing for [benunsworth.co.uk](https://benunsworth.co.uk) on iPhone, iPad, or Mac.

Once configured, tapping an icon on your Home Screen, pressing the iPhone Action Button, or tapping a Control Center tile triggers the GitHub Actions workflow to pull your `Ready to Publish` posts from Notion, optimise images, and publish them live to your site in around 60 seconds.

---

## 1. System Architecture

```
+-------------------------------------------------------------+
| 1. DRAFT IN NOTION (iPhone / iPad / Mac)                    |
|    - Write post using Digital Garden properties             |
|    - Embed photos directly from camera roll                 |
|    - Change 'Publish State' to "Ready to Publish"           |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 2. ONE-TAP TRIGGER                                          |
|    - Action Button / Home Screen / Control Center / Siri    |
|    - iOS Shortcut sends authenticated POST to GitHub API    |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 3. GITHUB ACTIONS (notion-publish.yml)                      |
|    - Downloads posts marked "Ready to Publish"              |
|    - Resizes & optimizes photos into public/images/posts/   |
|    - Creates _posts/YYYY-MM-DD-slug.md                      |
|    - Updates Notion status to "Published" + live URL        |
|    - Pushes commit to main -> GitHub Pages builds & deploys |
+-------------------------------------------------------------+
```

---

## 2. Generate a Fine-Grained Personal Access Token (PAT)

The iOS Shortcut needs an authenticated token to trigger your GitHub Actions workflow via the GitHub REST API. Using a **Fine-grained Personal Access Token** ensures the token is locked to this single repository with the absolute minimum permissions needed.

1. In your browser, go to [GitHub Token Settings](https://github.com/settings/tokens?type=beta) (or navigate to **Settings** > **Developer Settings** > **Personal access tokens** > **Fine-grained tokens**).
2. Click **Generate new token**.
3. Configure the token details:
   - **Token name:** `iOS Shortcut - Garden Publisher`
   - **Expiration:** Choose your preferred duration (e.g. `90 days`, `180 days`, or `1 year` — set a calendar reminder to regenerate).
   - **Resource owner:** Select your personal account (`benunsworth`).
   - **Repository access:** Choose **Only select repositories** > select `benunsworth/benunsworth.github.io`.
   - **Permissions:** Under **Repository permissions**, find **Actions** and select **Access: Read and write**. *(All other permissions should remain "No access")*.
4. Click **Generate token**.
5. Copy the generated token (`github_pat_...`) and store it safely in your password manager or iOS Notes. *(GitHub will not show it again).*

> [!NOTE]
> **Least Privilege Security:**
> The fine-grained token only needs `Actions: Read and write`. It does **not** need repository `Contents: Read and write` access because the workflow itself runs on GitHub with its own scoped credentials to commit posts to `main`.

---

## 3. Configure the iOS Shortcut

You can configure the Shortcut in under three minutes using Apple's built-in **Shortcuts** app on iOS, iPadOS, or macOS.

### Step-by-Step Action Configuration

1. Open the **Shortcuts** app on your iPhone or iPad.
2. Tap **+** in the top right to create a new shortcut.
3. Tap the shortcut title at the top, select **Rename**, and name it:
   `Publish Garden`
4. Tap the icon next to the title to customize it:
   - **Colour:** Terracotta / Orange
   - **Glyph:** Sprout / Leaf or Rocket
5. Add the following actions in sequence:

#### Action 1: Define Your Token (Text)
- Search for and add the **Text** action.
- Paste your fine-grained token (`github_pat_...`) into the text box.

#### Action 2: Get Contents of URL (HTTP POST)
- Search for and add the **Get Contents of URL** action.
- Set the **URL** to:
  ```text
  https://api.github.com/repos/benunsworth/benunsworth.github.io/actions/workflows/notion-publish.yml/dispatches
  ```
- Tap the expand arrow (`>`) on the action to reveal request options:
  - **Method:** `POST`
  - **Headers:** Add three headers:
    | Key | Value |
    | :--- | :--- |
    | `Accept` | `application/vnd.github+json` |
    | `Authorization` | `Bearer ` *(insert the Text variable from Action 1 right after `Bearer `)* |
    | `X-GitHub-Api-Version` | `2022-11-28` |
  - **Request Body:** Select **JSON**
  - Tap **Add new field** > choose **Text**:
    - **Key:** `ref`
    - **Value:** `main`

#### Action 3: Notify Success
- Search for and add the **Show Notification** action:
  - Set the message to:
    `Publishing garden post from Notion... Live in ~60 seconds.`
  - Optional title: `Garden Publisher`

#### Action 4: (Optional) Haptic Feedback
- Search for and add the **Vibrate Device** action for subtle tactile confirmation when tapped.

---

### Shortcut Summary View

When complete, your Shortcut should match this layout:

```text
[Text]
  github_pat_11A...

[Get contents of https://api.github.com/repos/benunsworth/benunsworth.github.io/actions/workflows/notion-publish.yml/dispatches]
  Method: POST
  Headers:
    Accept: application/vnd.github+json
    Authorization: Bearer [Text]
    X-GitHub-Api-Version: 2022-11-28
  Request Body: JSON
    ref: main

[Show Notification]
  "Publishing garden post from Notion... Live in ~60 seconds."

[Vibrate Device]
```

---

## 4. Mobile Hardware & System Triggers

Once your shortcut is created, set up single-tap access wherever it is most convenient:

### Option A: iPhone Action Button (iPhone 15 Pro / 16 / 16 Pro)
1. Go to iPhone **Settings** > **Action Button**.
2. Swipe across to select **Shortcut**.
3. Tap the selection menu and choose **Publish Garden**.
4. Now, pressing and holding the Action Button immediately fires the publishing workflow.

### Option B: Home Screen Icon
1. In the **Shortcuts** app, long-press or tap `...` on **Publish Garden**.
2. Tap the Share sheet button (or the `i` Details inspector).
3. Tap **Add to Home Screen**.
4. Choose an icon photo or glyph and tap **Add**.
5. Place the icon beside your Notion app on your Home Screen.

### Option C: iOS 18 Control Center Tile
1. Swipe down from the top-right corner to open **Control Center**.
2. Press and hold in an empty space to enter edit mode, then tap **+ Add a Control** at the bottom.
3. Search for **Shortcut** and add the 1×1 tile.
4. Tap the tile to assign **Publish Garden**.

### Option D: Siri Voice Trigger
Because the shortcut is named **Publish Garden**, you can activate it hands-free at any time:
> *"Hey Siri, Publish Garden"*

### Option E: Back Tap (Accessibility)
1. Go to **Settings** > **Accessibility** > **Touch** > **Back Tap**.
2. Select **Double Tap** or **Triple Tap**.
3. Scroll down to the Shortcuts section and select **Publish Garden**.

---

## 5. Alternative: Zero-PAT Trigger via GitHub Mobile

If you prefer not to manage a Personal Access Token, you can trigger the publishing workflow directly from the official **GitHub Mobile** app on iOS using your standard biometric login (Face ID / Touch ID):

1. Install the official **GitHub** app from the iOS App Store and sign in.
2. In GitHub Mobile, navigate to your repository: `benunsworth/benunsworth.github.io`.
3. Tap **Actions** in the repository tabs.
4. Tap **Publish from Notion**.
5. Tap the overflow menu (`...`) or the blue **Run workflow** button.
6. Leave the branch as `main` and tap **Run workflow**.

---

## 6. Testing & Verification

### Test via Terminal (cURL)
Before running the shortcut on your phone, you can verify your token and endpoint using this cURL command in your terminal:

```bash
curl -i -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_GITHUB_PAT" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/benunsworth/benunsworth.github.io/actions/workflows/notion-publish.yml/dispatches \
  -d '{"ref":"main"}'
```

**Expected Response:**
```http
HTTP/2 204 No Content
```
A `204 No Content` response indicates GitHub accepted the dispatch event and has queued the workflow.

### End-to-End Test Workflow
1. Open your Notion blog database.
2. Create a test note (e.g. `Type: note`, `Status: rough`, `Title: Mobile Publishing Test`).
3. Set `Publish State` to **Ready to Publish**.
4. Trigger your **Publish Garden** shortcut (or run the cURL command).
5. Watch your phone notification appear.
6. Visit `https://github.com/benunsworth/benunsworth.github.io/actions` to see the **Publish from Notion** workflow run.
7. Within ~60 seconds, check [benunsworth.co.uk](https://benunsworth.co.uk) to see your new post live!

---

## 7. Troubleshooting & Status Codes

| HTTP Status Code | Meaning | What to Check |
| :--- | :--- | :--- |
| **`204 No Content`** | **Success** | Workflow triggered and queued. Check GitHub Actions tab for progress. |
| **`401 Unauthorized`** | Invalid Token | The PAT is mistyped, expired, or revoked. Check the `Authorization: Bearer <TOKEN>` header. |
| **`403 Forbidden`** | Insufficient Scope | The PAT lacks permissions. Ensure **Actions: Read and write** is granted for `benunsworth/benunsworth.github.io`. |
| **`404 Not Found`** | Resource Not Found | Check for typos in the URL. Ensure the workflow file is committed to `main` at `.github/workflows/notion-publish.yml`. |
| **`422 Unprocessable`** | Invalid Payload | Ensure request body is JSON and contains `{"ref": "main"}`. |
