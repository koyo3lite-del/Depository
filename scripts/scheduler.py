"""
Main scheduler/dispatcher for the Depository auto-posting system.

Loads today's post and dispatches it to each configured platform.
Intended to be triggered by a daily cron job or GitHub Actions workflow.
"""

import logging
import sys
from datetime import date
from pathlib import Path

# Allow running as __main__ from the scripts/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import load_platforms, load_post_for_date, load_settings, setup_logging

logger = logging.getLogger("depository.scheduler")


def dispatch(target_date: date | None = None, dry_run: bool | None = None) -> None:
    """
    Load the post for *target_date* and send it to all enabled platforms.

    Parameters
    ----------
    target_date: Date of the post to dispatch. Defaults to today.
    dry_run:     Override the dry_run setting from config/settings.json.
    """
    settings = load_settings()
    platforms = load_platforms()

    if dry_run is None:
        dry_run = settings.get("dry_run", False)

    if target_date is None:
        target_date = date.today()

    logger.info("Running scheduler for date: %s (dry_run=%s)", target_date, dry_run)

    post = load_post_for_date(target_date)
    if post is None:
        logger.warning("No post file found for %s. Nothing to publish.", target_date)
        return

    post_platforms = post.get("platforms", [])
    if not post_platforms:
        logger.warning("Post for %s has no platforms configured. Skipping.", target_date)
        return

    errors: list[str] = []

    if "twitter" in post_platforms:
        twitter_cfg = platforms.get("twitter", {})
        if twitter_cfg.get("enabled", False):
            try:
                from post_to_twitter import post_tweet  # noqa: PLC0415
                post_tweet(post["text"], dry_run=dry_run)
            except Exception as exc:  # noqa: BLE001
                logger.error("Failed to post to Twitter: %s", exc)
                errors.append(f"twitter: {exc}")
        else:
            logger.info("Twitter platform is disabled in config. Skipping.")

    if "instagram" in post_platforms:
        ig_cfg = platforms.get("instagram", {})
        if ig_cfg.get("enabled", False):
            try:
                from post_to_instagram import post_to_instagram  # noqa: PLC0415
                post_to_instagram(
                    caption=post.get("instagram_caption", post["text"]),
                    image_url=post.get("image_url"),
                    dry_run=dry_run,
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("Failed to post to Instagram: %s", exc)
                errors.append(f"instagram: {exc}")
        else:
            logger.info("Instagram platform is disabled in config. Skipping.")

    if errors:
        logger.error("Dispatch completed with errors: %s", "; ".join(errors))
        sys.exit(1)

    logger.info("Dispatch completed successfully for %s.", target_date)


if __name__ == "__main__":
    import argparse

    setup_logging()
    parser = argparse.ArgumentParser(
        description="Dispatch today's post to all configured social media platforms."
    )
    parser.add_argument("--date", help="Date to post (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--dry-run", action="store_true", help="Log without posting.")
    args = parser.parse_args()

    settings = load_settings()
    target = date.fromisoformat(args.date) if args.date else date.today()
    dry_run_flag = args.dry_run or settings.get("dry_run", False)

    dispatch(target_date=target, dry_run=dry_run_flag)
