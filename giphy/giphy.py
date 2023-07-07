from __future__ import annotations
import httpx
from .parsers import Gif, Channel, Term, Category, Sticker as StickerParser, Emoji as EmojiParser
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


class GIF:
    BaseUrl = "https://api.giphy.com/v1/gifs/"
    UrlTrending = "https://api.giphy.com/v1/trending/searches"
    UrlTag = "https://api.giphy.com/v1/tags/related/"
    UrlChannel = "https://api.giphy.com/v1/channels/search"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def trending(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        rating: Optional[str] = None,
        random_id: Optional[str] = None,
        bundle: Optional["str"] = None,
    ) -> list[Gif]:
        params = {
            "api_key": self.api_key,
            "limit": limit,
            "offset": offset,
            "rating": rating,
            "random_id": random_id,
            "bundle": bundle,
        }
        data = httpx.get(f"{self.BaseUrl}trending", params=params).json()["data"]
        return [Gif(data[i]) for i in range(len(data))]

    def search(
        self,
        q: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        rating: Optional[str] = None,
        lang: Optional[str] = None,
        random_id: Optional[str] = None,
        bundle: Optional["str"] = None,
    ) -> list[Gif]:
        params = {
            "api_key": self.api_key,
            "q": q,
            "limit": limit,
            "offset": offset,
            "rating": rating,
            "lang": lang,
            "random_id": random_id,
            "bundle": bundle,
        }
        data = httpx.get(f"{self.BaseUrl}search", params=params).json()["data"]
        return [Gif(data[i]) for i in range(len(data))]

    def translate(
        self,
        s: str,
        *,
        random_id: Optional[str] = None,
        weirdness: int = 1,
    ) -> Gif:
        params = {
            "api_key": self.api_key,
            "s": s,
            "random_id": random_id,
            "weirdness": weirdness,
        }
        return Gif(httpx.get(f"{self.BaseUrl}random", params=params).json()["data"])

    def random(
        self,
        tag: Optional[str] = None,
        *,
        rating: Optional[str] = None,
        random_id: Optional[str] = None,
    ) -> Gif:
        params = {
            "api_key": self.api_key,
            "tag": tag,
            "rating": rating,
            "random_id": random_id,
        }
        return Gif(httpx.get(f"{self.BaseUrl}random", params=params).json()["data"])


    def get_random_id( #Might need to change this elsewhere
        self
    ):
        params = {
            "api_key": self.api_key,
        }
        return httpx.get(f"{self.BaseUrl}random", params=params).json()

    def fetch(
        self, id: int, *, random_id: Optional[str] = None, rating: Optional[str] = None
    ):
        params = {
            "api_key": self.api_key,
            "gif_id": id,
            "random_id": random_id,
            "rating": rating,
        }
        data = httpx.get(self.BaseUrl + id, params=params).json()
        return Gif(data["data"])

    def fetch_many(
        self,
        ids: list[int],
        *,
        random_id: Optional[str] = None,
        rating: Optional[str] = None,
    ):
        params = {"api_key": self.api_key, "random_id": random_id, "rating": rating}
        _ids = ""
        for id in ids:
            if ids[-1] == id:
                _ids += id
                break
            _ids += id + ", "

        params["ids"] = _ids
        return [Gif(data) for data in httpx.get(
            self.BaseUrl[:-1], params=params
        ).json()["data"]]  # Put index slice: Might need to change the BaseUrl var without '/' at the ending.

    def fetch_searches(
        self,
    ):  # Might need to move this method elsewhere for now this staying here!
        params = {"api_key": self.api_key}
        return httpx.get(self.UrlTrending, params=params).json()["data"]

    def fetch_relate_search(self, term: str): 
        params = {"api_key": self.api_key, "term": term}

        return httpx.get(self.UrlTag + term, params=params).json()["data"]["name"]

    def fetch_channels(
        # Might need to move this method elsewhere for now this staying here!
        self, q: str, *, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[Optional[Channel]]:
        params = {
            "api_key": self.api_key, 
            "q": q,
            "limit": limit, 
            "offset": offset
        }
        res = httpx.get(self.UrlChannel, params=params).json()["data"]
        if not res:
            return []
        return [Channel(data) for data in res]

    def fetch_tag_autocomplete(
        # Might need to move this method elsewhere for now this staying here!
        self, q: str, *, limit: Optional[int] = None, offset: Optional[int] = None
    ):
        params = {"api_key": self.api_key, "q": q, "limit": limit, "offset": offset}

        return [Term(data) for data in httpx.get(self.BaseUrl + "search/tags", params=params).json()["data"]]

    def fetch_categories(self): 
        # Might need to move this method elsewhere for now this staying here!
        params = {"api_key": self.api_key}

        return  [Category(data) for data in httpx.get(self.BaseUrl + "categories", params=params).json()["data"]]


class Sticker:
    BaseUrl = "https://api.giphy.com/v1/stickers/"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_trending(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        rating: Optional[str] = None,
    ):
        params = {
            "api_key": self.api_key,
            "limit": limit,
            "offset": offset,
            "rating": rating,
        }
        return [StickerParser(data) for data in httpx.get(f"{self.BaseUrl}trending", params=params).json()["data"]]

    def search(
        self,
        q: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        rating: Optional[str] = None,
    ):
        params = {
            "api_key": self.api_key,
            "q": q,
            "limit": limit,
            "offset": offset,
            "rating": rating,
        }
        return [StickerParser(data) for data in httpx.get(f"{self.BaseUrl}trending", params=params).json()["data"]]

    def translate(
        self,
        s: str,
        *,
        weirdness=1,
    ):
        params = {
            "api_key": self.api_key,
            "s": s,
            "weirdness": weirdness,
        }
        return StickerParser(httpx.get(f"{self.BaseUrl}translate", params=params).json()["data"])


    def random(
        self,
        tag: Optional[str] = None,
        *,
        rating: Optional[str] = None,
        random_id: Optional[str] = None,
    ) -> Gif:
        params = {
            "api_key": self.api_key,
            "tag": tag,
            "rating": rating,
            "random_id": random_id,
        }
        return StickerParser(httpx.get(f"{self.BaseUrl}translate", params=params).json()["data"])


class Emoji:
    BaseUrl = "https://api.giphy.com/v2/emoji"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch(self, *, limit: Optional[int] = None, offset: Optional[int] = None):
        params = {"api_key": self.api_key, "limit": limit, "offset": offset}

        return [EmojiParser(data) for data in httpx.get(self.BaseUrl, params=params).json()["data"]]

    def get_variations(self, *, gif_id: Optional[int]):
        params = {"api_key": self.api_key}
        data = httpx.get(self.BaseUrl+f"/{gif_id}/variations", params=params).json()["data"]
        if not data:
            return None
        return EmojiParser(data)
