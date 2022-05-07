from dataclasses import dataclass
import os
from typing import Any, Dict
from requests import Response, Session
from viz_image_unobfuscate import unobfuscate_image
from PIL import Image


@dataclass
class Manifest:
    metadata_url: str
    pages: Dict[str, str]


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

    def _get_metadata(self, manifest: Manifest) -> Dict:
        resp: Response = self.session.get(manifest.metadata_url)
        return resp.json()

    def _get_page_image(self, url: str) -> Image:
        resp: Response = self.session.get(url, stream=True)

        tmp_filename: str = "tmp.jpg"
        with open(tmp_filename, "wb") as file_handle:
            for chunk in resp:
                file_handle.write(chunk)

        image: Image = unobfuscate_image(tmp_filename)

        os.remove(tmp_filename)  # remove temporary image

        return image

    def _save_pages(self, manifest: Manifest, directory: str) -> None:
        for page_num, url in manifest.pages.items():
            filename = os.path.join(directory, f"page{page_num}.jpg")
            image: Image = self._get_page_image(url)
            image.save(filename)

    def save_chapter(self, chapter_id: int, directory: str) -> None:
        manifest: Manifest = self._get_manifest(chapter_id)
        # resp = self._get_metadata(manifest)
        self._save_pages(manifest, directory)


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

    args = parser.parse_args()

    chapter_id = 24297
    viz = VizManga()
    viz.save_chapter(args.chapter_id, args.directory)
