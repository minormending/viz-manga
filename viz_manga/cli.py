import logging
import os
from typing import List

from viz_manga import VizMangaFetch, VizMangaDetails
from viz_manga.manga_details import Series


def get_all_series(series: Series, directory: str) -> None:
    viz: VizMangaFetch = VizMangaFetch()
    details: VizMangaDetails = VizMangaDetails()
    for chapter in details.get_series_chapters(series):
        if chapter.is_free:
            chapter_directory: str = os.path.join(
                directory, chapter.title or chapter.id
            )
            if os.path.exists(chapter_directory):
                logging.warning(
                    f"Directory {chapter_directory} for chapter {chapter.title} already exists, skipping."
                )
            else:
                os.mkdir(chapter_directory)
                if os.path.exists(chapter_directory):
                    if viz.save_chapter(chapter.id, chapter_directory, combine=True):
                        logging.info(
                            f"Successfully retrieved chapter {chapter.title} at: {chapter_directory}"
                        )
                    else:
                        logging.warning(
                            f"Unable to retrieved chapter {chapter.title} and save in {chapter_directory}"
                        )
                else:
                    logging.warning(
                        f"Unable to create directory {chapter_directory} for chapter {chapter.title}, skipping."
                    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Lookup Viz manga information.")
    subparsers = parser.add_subparsers(dest="command")

    fetch_chapter = subparsers.add_parser(
        "fetch", help="Fetches and deobfuscates an entire manga chapter for reading."
    )
    fetch_chapter.add_argument(
        "slug", help="Chapter id or series name obtained from the Viz site."
    )
    fetch_chapter.add_argument(
        "--directory",
        default=".",
        help="Output directory to save the deobfuscated pages.",
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

        if args.slug.isnumeric():
            chapter_id: int = int(args.slug)
            viz: VizMangaFetch = VizMangaFetch()
            if viz.save_chapter(chapter_id, args.directory, combine=True):
                logging.info(f"Successfully retrieved chapter {chapter_id}")
            else:
                logging.error(f"Failed to retrieve chapter {chapter_id}")
        else:
            series: Series = Series(None, slug=args.slug)
            get_all_series(series, args.directory)
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
