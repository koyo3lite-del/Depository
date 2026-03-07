# Depository

An automated social media posting system that publishes daily content to **Twitter/X** and **Instagram** using a GitHub Actions workflow.

## How It Works

1. Content is written as JSON files under `content/posts/` — one file per day (e.g. `2026-03-01.json`).
2. A GitHub Actions workflow (`autopost.yml`) runs every day at **12:00 UTC**, reads today's post file, and dispatches it to each configured platform.
3. The workflow can also be triggered manually with an optional date override and dry-run mode.

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── autopost.yml       # Daily cron workflow
├── config/
│   ├── platforms.json         # Platform API configuration
│   └── settings.json          # General settings
├── content/
│   └── posts/
│       └── YYYY-MM-DD.json    # One post file per day
└── scripts/
    ├── utils.py               # Shared helpers
    ├── post_to_twitter.py     # Twitter/X posting logic
    ├── post_to_instagram.py   # Instagram posting logic
    └── scheduler.py           # Main dispatcher
```

## Post File Format

Create a file in `content/posts/` named `YYYY-MM-DD.json`:

```json
{
  "date": "2026-03-01",
  "platforms": ["twitter", "instagram"],
  "text": "Your tweet text here (max 280 chars) #Hashtag",
  "instagram_caption": "Your Instagram caption here ✨\n\n#Hashtag",
  "image_url": "https://example.com/image.jpg",
  "tags": ["Hashtag"]
}
```

| Field                | Required | Description |
|----------------------|----------|-------------|
| `date`               | Yes      | ISO date matching the filename |
| `platforms`          | Yes      | List of platforms to post to (`twitter`, `instagram`) |
| `text`               | Yes      | Post body (used for Twitter; fallback for Instagram) |
| `instagram_caption`  | No       | Instagram-specific caption (falls back to `text`) |
| `image_url`          | No       | Publicly accessible image URL (required for Instagram feed posts) |
| `tags`               | No       | Tag list for reference |

## Configuration

### `config/settings.json`

| Key                   | Description |
|-----------------------|-------------|
| `timezone`            | Display timezone (informational) |
| `dry_run`             | If `true`, log posts without sending |
| `content_dir`         | Path to post files (relative to repo root) |
| `log_level`           | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `retry_attempts`      | Number of API call retries |
| `retry_delay_seconds` | Seconds to wait between retries |

### `config/platforms.json`

Stores the names of the environment variables used for API credentials. **Do not store actual secrets here** — use GitHub repository secrets instead.

## GitHub Secrets Required

| Secret                          | Platform   | Description |
|---------------------------------|------------|-------------|
| `TWITTER_API_KEY`               | Twitter/X  | API key (consumer key) |
| `TWITTER_API_SECRET`            | Twitter/X  | API secret |
| `TWITTER_ACCESS_TOKEN`          | Twitter/X  | OAuth access token |
| `TWITTER_ACCESS_TOKEN_SECRET`   | Twitter/X  | OAuth access token secret |
| `TWITTER_BEARER_TOKEN`          | Twitter/X  | Bearer token (v2 read operations) |
| `INSTAGRAM_ACCESS_TOKEN`        | Instagram  | Facebook Graph API access token |
| `INSTAGRAM_USER_ID`             | Instagram  | Instagram Business/Creator user ID |

Go to **Settings → Secrets and variables → Actions** in your GitHub repository to add these.

## Running Locally

Install dependencies:

```bash
pip install requests requests-oauthlib
```

Post today's content (dry run):

```bash
python scripts/scheduler.py --dry-run
```

Post for a specific date:

```bash
python scripts/scheduler.py --date 2026-03-01
```

Post only to Twitter:

```bash
python scripts/post_to_twitter.py --date 2026-03-01 --dry-run
```

Post only to Instagram:

```bash
python scripts/post_to_instagram.py --date 2026-03-01 --dry-run
```

## Manual Workflow Trigger

In GitHub, go to **Actions → Auto-Post to Social Media → Run workflow** and optionally provide:

- **Date** – a specific `YYYY-MM-DD` date (leave blank for today)
- **Dry run** – set to `true` to log without actually posting
