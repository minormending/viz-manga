from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
from requests import Response, Session
from viz_image_unobfuscate import unobfuscate_image
from PIL import Image
import os


@dataclass
class Manifest:
    metadata_url: str
    pages: Dict[str, str]


@dataclass
class Metadata:
    title: str
    width: int
    height: int
    spreads: List[int]
    pages: List[Any]  # seems to always be empty


class VizManga:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
        }
        self.session.proxies = {"http": "127.0.0.1:8888", "https": "127.0.0.1:8888"}
        self.session.verify = False

    def _get_manifest(self, chapter_id: int) -> Manifest:
        # if we ask for more pages than are in the chapter, the endpoint will return the max pages
        pages: str = ",".join([str(i) for i in range(25)])
        url: str = f"https://www.viz.com/manga/get_manga_url?device_id=3&manga_id={chapter_id}&pages={pages}"
        headers: Dict[str, str] = {
            "Referer": "https://www.viz.com/shonenjump/?action=read",
        }
        resp: Response = self.session.get(url, headers=headers)
        payload: Dict[str, Any] = resp.json()
        return Manifest(payload.get("metadata"), payload.get("data"))

    def _get_metadata(self, manifest: Manifest) -> Metadata:
        resp: Response = self.session.get(manifest.metadata_url)
        return Metadata(**resp.json())

    def _get_page_image(self, url: str) -> Image:
        resp: Response = self.session.get(url, stream=True)

        tmp_filename: str = "tmp.jpg"
        with open(tmp_filename, "wb") as file_handle:
            for chunk in resp:
                file_handle.write(chunk)

        image: Image = unobfuscate_image(tmp_filename)

        os.remove(tmp_filename)  # remove temporary image

        return image

    def _save_pages(self, manifest: Manifest, directory: str) -> List[str]:
        page_names: List[str] = []
        for page_num, url in manifest.pages.items():
            filename = os.path.join(directory, f"page{int(page_num):02d}.jpg")
            image: Image = self._get_page_image(url)
            image.save(filename)
            page_names.append(filename)
        return page_names

    def save_chapter(self, chapter_id: int, directory: str, combine: bool) -> None:
        manifest: Manifest = self._get_manifest(chapter_id)
        # needs to be done immediated b/c url only signed for 1 sec from when it leaves the Viz server.
        metadata = self._get_metadata(manifest)
        # each page url is signed for 1 second longer than the previous page.
        page_names: List[str] = self._save_pages(manifest, directory)

        if combine:
            pages_combine: List[int] = list(range(0, len(page_names), 2))  # all pages
        elif metadata.spreads:
            pages_combine: List[int] = metadata.spreads

        for idx_right in pages_combine:
            filename_left: str = page_names[idx_right + 1]
            filename_right: str = page_names[idx_right]
            filename: str = os.path.join(
                directory, f"page{idx_right:02d}_{idx_right + 1:02d}.jpg"
            )
            combined_image: Image = self._combine_pages(filename_left, filename_right)
            combined_image.save(filename)

            os.remove(filename_left)
            os.remove(filename_right)

    def _combine_pages(self, page_left: str, page_right: str) -> Image:
        image_left: Image = Image.open(page_left)
        image_right: Image = Image.open(page_right)

        size: Tuple[int, int] = (
            image_left.width + image_right.width,
            max(image_left.height, image_right.height),
        )
        combined_image: Image = Image.new("RGB", size, "white")
        combined_image.paste(image_left, (0, 0))
        combined_image.paste(image_right, (image_left.width, 0))
        return combined_image


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Unobfuscates an entire manga chapter for reading."
    )
    parser.add_argument(
        "chapter_id", type=int, help="Chapter id obtained from the Viz site."
    )
    parser.add_argument(
        "--directory",
        default=".",
        help="Output directory to save the unobfuscated pages.",
    )
    parser.add_argument(
        "--combine",
        action="store_true",
        help="Combine left and right pages and spreads into 1 image.",
    )

    args = parser.parse_args()

    chapter_id = 24297
    viz = VizManga()
    viz.save_chapter(args.chapter_id, args.directory, args.combine)
