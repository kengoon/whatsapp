import mimetypes
from typing_extensions import Optional
import requests
from whatsapp.errors import Handle
from whatsapp.models import Media, MediaResponse, WhatsappConfig


class WhatsappMedia:
    def __init__(self, config: WhatsappConfig):
        self.config = config

    def upload_media(self, file_path: str, mime_type: str = None) -> MediaResponse:
        if mime_type is None:
            mime_type = mimetypes.guess_type(file_path)[0]
        media = Media(file=file_path, type=mime_type)
        files = {
            "file": (media.file.name, open(file_path, "rb"), mime_type),
        }
        r = requests.post(
            f"{self.config.api_url}/media",
            headers=self.config.headers,
            files=files,
            data={"messaging_product": "whatsapp"}
        )
        if r.status_code != 200:
            Handle(r.json())
        return MediaResponse(**r.json())

    def download_media(self, media_url: str, save: bool = True) -> Optional[tuple[str, bytes]]:
        #
        r = requests.get(media_url, headers=self.config.headers)
        r.raise_for_status()
        filename = r.headers["Content-Disposition"].split("=")[1]
        if save:
            with open(filename, "wb") as f:
                f.write(r.content)
        else:
            return filename, r.content

    def query_media_url(self, media_id: str) -> MediaResponse:
        url = str(self.config.api_url).split(f"{self.config.phone_number_id}")[0] + media_id + "/"
        r = requests.get(url, headers=self.config.headers)
        if r.status_code != 200:
            Handle(r.json())
        return MediaResponse(**r.json())

    def delete_media(self, media_id: str) -> MediaResponse:
        url = str(self.config.api_url).split(f"{self.config.phone_number_id}")[0] + media_id + "/"
        r = requests.delete(url, headers=self.config.headers)
        if r.status_code != 200:
            Handle(r.json())
        return MediaResponse(**r.json())
