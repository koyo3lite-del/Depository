"""Post content to Instagram using the Facebook Graph API."""

import logging
import sys
from pathlib import Path

import requests

# Allow running the script directly from the scripts/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import get_env, load_platforms, load_settings, retry, setup_logging

logger = logging.getLogger("depository.instagram")


def _graph_url(version: str, path: str, base: str) -> str:
    return f"{base}/{version}/{path}"


def _create_media_container(
    user_id: str,
    access_token: str,
    caption: str,
    image_url: str | None,
    api_version: str,
    api_base: str,
) -> str:
    """
    Create an Instagram media container.
    Returns the container ID.
    """
    url = _graph_url(api_version, f"{user_id}/media", api_base)
    params: dict = {"caption": caption, "access_token": access_token}

    if image_url:
        params["image_url"] = image_url
        params["media_type"] = "IMAGE"
    else:
        # Text-only posts are not supported directly; use a placeholder approach.
        # In production, supply an image_url for every Instagram post.
        raise ValueError(
            "Instagram requires an image_url for feed posts. "
            "Provide 'image_url' in the post JSON."
        )

    response = requests.post(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["id"]


def _publish_media_container(
    user_id: str,
    access_token: str,
    container_id: str,
    api_version: str,
    api_base: str,
) -> dict:
    """Publish a previously created media container."""
    url = _graph_url(api_version, f"{user_id}/media_publish", api_base)
    params = {
        "creation_id": container_id,
        "access_token": access_token,
    }
    response = requests.post(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def post_to_instagram(
    caption: str,
    image_url: str | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Post an image with caption to Instagram.

    Parameters
    ----------
    caption:   The post caption / text.
    image_url: Publicly accessible URL to the image to post.
    dry_run:   When True, log without actually sending.
    """
    platforms = load_platforms()
    settings = load_settings()
    ig_cfg = platforms["instagram"]

    if dry_run:
        logger.info(
            "[DRY RUN] Would post to Instagram. Caption: %s | Image URL: %s",
            caption,
            image_url,
        )
        return {"dry_run": True, "caption": caption, "image_url": image_url}

    access_token = get_env(ig_cfg["access_token_env"])
    user_id = get_env(ig_cfg["user_id_env"])
    api_version = ig_cfg.get("graph_api_version", "v18.0")
    api_base = ig_cfg.get("graph_api_base", "https://graph.facebook.com")

    attempts = settings.get("retry_attempts", 3)
    delay = settings.get("retry_delay_seconds", 5)

    def _send():
        container_id = _create_media_container(
            user_id, access_token, caption, image_url, api_version, api_base
        )
        return _publish_media_container(
            user_id, access_token, container_id, api_version, api_base
        )

    result = retry(_send, attempts=attempts, delay=delay)
    logger.info("Instagram post published successfully. Response: %s", result)
    return result


if __name__ == "__main__":
    import argparse
    from datetime import date

    from utils import load_post_for_date, load_settings

    setup_logging()
    parser = argparse.ArgumentParser(description="Post today's content to Instagram.")
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

    if "instagram" not in post.get("platforms", []):
        logger.info("Post for %s is not configured for Instagram. Skipping.", target)
        sys.exit(0)

    post_to_instagram(
        caption=post.get("instagram_caption", post["text"]),
        image_url=post.get("image_url"),
        dry_run=dry_run,
    )
