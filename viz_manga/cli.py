import logging
from typing import List

from viz_manga import VizMangaFetch, VizMangaDetails
from viz_manga.manga_details import Series


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Lookup Viz manga information.")
    subparsers = parser.add_subparsers(dest="command")

    fetch_chapter = subparsers.add_parser(
        "fetch",
        help="Fetches and deobfuscates an entire manga chapter for reading."
    )
    fetch_chapter.add_argument(
        "chapter_id", type=int, help="Chapter id obtained from the Viz site."
    )
    fetch_chapter.add_argument(
        "--directory",
        default=".",
        help="Output directory to save the deobfuscated pages.",
    )
    fetch_chapter.add_argument(
        "--combine",
        action="store_true",
        help="Combine left and right pages into one image.",
    )

    series_parser = subparsers.add_parser(
        "series",
        help="Get series title and slug (for chapter lookup) obtained from the Viz site.",
    )

    chapter_parser = subparsers.add_parser(
        "chapters", help="Get chapter title and id obtained from the Viz site."
    )
    chapter_parser.add_argument(
        "series_slug",
        help="Series title for which to lookup chapter ids from the Viz site.",
    )
    chapter_parser.add_argument(
        "--free",
        action="store_true",
        help="Only show publicly available free chapters for the series.",
    )

    args = parser.parse_args()

    if args.command.lower() == "fetch":
        logging.basicConfig(level=logging.INFO)
        viz: VizMangaFetch = VizMangaFetch()
        if viz.save_chapter(args.chapter_id, args.directory, args.combine):
            print(f"Successfully retrieved chapter {args.chapter_id}")
        else:
            print(f"Failed to retrieve chapter {args.chapter_id}")
    elif args.command.lower() == "series":
        details: VizMangaDetails = VizMangaDetails()
        series: List[Series] = details.get_series()
        for manga in series:
            print(manga.__dict__)
    elif args.command.lower() == "chapters" and args.series_slug:
        details: VizMangaDetails = VizMangaDetails()
        show_free_only: bool = args.free
        for chapter in details.get_series_chapters(Series(None, args.series_slug)):
            if not show_free_only or chapter.is_free:
                print(chapter.__dict__)


if __name__ == "__main__":
    main()