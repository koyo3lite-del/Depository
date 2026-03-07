"""Post content to Twitter/X using the Twitter API v2."""

import logging
import sys
from pathlib import Path

import requests

# Allow running the script directly from the scripts/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import get_env, load_platforms, load_settings, retry, setup_logging

logger = logging.getLogger("depository.twitter")


def _build_headers(bearer_token: str) -> dict:
    return {"Authorization": f"Bearer {bearer_token}"}


def _oauth1_auth(api_key: str, api_secret: str, token: str, token_secret: str):
    """Return a requests-compatible OAuth 1.0a auth object."""
    try:
        from requests_oauthlib import OAuth1  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "requests-oauthlib is required for Twitter OAuth 1.0a. "
            "Install it with: pip install requests-oauthlib"
        ) from exc
    return OAuth1(api_key, api_secret, token, token_secret)


def post_tweet(text: str, dry_run: bool = False) -> dict:
    """
    Post a tweet and return the API response.

    Parameters
    ----------
    text:    The tweet text (max 280 characters).
    dry_run: When True, log the tweet without actually sending it.
    """
    platforms = load_platforms()
    settings = load_settings()
    twitter_cfg = platforms["twitter"]
    max_length = twitter_cfg.get("max_tweet_length", 280)

    if len(text) > max_length:
        logger.warning(
            "Tweet text is %d characters (max %d); it will be truncated.",
            len(text),
            max_length,
        )
        text = text[:max_length]

    if dry_run:
        logger.info("[DRY RUN] Would post tweet: %s", text)
        return {"dry_run": True, "text": text}

    api_key = get_env(twitter_cfg["api_key_env"])
    api_secret = get_env(twitter_cfg["api_secret_env"])
    access_token = get_env(twitter_cfg["access_token_env"])
    access_token_secret = get_env(twitter_cfg["access_token_secret_env"])

    auth = _oauth1_auth(api_key, api_secret, access_token, access_token_secret)
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}

    attempts = settings.get("retry_attempts", 3)
    delay = settings.get("retry_delay_seconds", 5)

    def _send():
        response = requests.post(url, json=payload, auth=auth, timeout=30)
        response.raise_for_status()
        return response.json()

    result = retry(_send, attempts=attempts, delay=delay)
    logger.info("Tweet posted successfully. Response: %s", result)
    return result


if __name__ == "__main__":
    import argparse
    from datetime import date

    # Allow importing load_post_for_date when running as __main__
    from utils import load_post_for_date, load_settings

    setup_logging()
    parser = argparse.ArgumentParser(description="Post today's content to Twitter/X.")
    parser.add_argument("--date", help="Date to post (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--dry-run", action="store_true", help="Log without posting.")
    args = parser.parse_args()

    target = date.fromisoformat(args.date) if args.date else date.today()
    settings = load_settings()
    dry_run = args.dry_run or settings.get("dry_run", False)

    post = load_post_for_date(target)
    if post is None:
        logger.error("No post found for %s", target)
        sys.exit(1)

    if "twitter" not in post.get("platforms", []):
        logger.info("Post for %s is not configured for Twitter. Skipping.", target)
        sys.exit(0)

    post_tweet(post["text"], dry_run=dry_run)
