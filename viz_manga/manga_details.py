from bs4 import BeautifulSoup
from requests import Response, Session


class VizMangaDetails:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
        }

    def get_series(self) -> None:
        url: str = "https://www.viz.com/shonenjump"
        resp: Response = self.session.get(url)

        soup: BeautifulSoup = BeautifulSoup(resp.text, "html.parser")
