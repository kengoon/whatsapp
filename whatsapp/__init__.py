import requests
from bs4 import BeautifulSoup
from whatsapp.models import WhatsappConfig
from whatsapp.media import WhatsappMedia
from whatsapp.message import WhatsAppMessage
from whatsapp.models import WhatsappConfig


__all__ = ("WhatsApp",)


class WhatsApp:
    def __init__(self, token: str, phone_number_id: str, verify_token: str, version: str = "latest"):
        version = self._init_api_version(version)
        self.config = WhatsappConfig(
            token=token,
            phone_number_id=phone_number_id,
            verify_token=verify_token,
            version=version,
            api_url=f"https://graph.facebook.com/{self.version}/{self.config.phone_number_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.media = WhatsappMedia(self.config)
        self.message = WhatsAppMessage(self.config)

    @staticmethod
    def _init_api_version(version: str):
        if version == "latest":
            r = requests.get("https://developers.facebook.com/docs/graph-api/changelog/")
            soup = BeautifulSoup(r.text, features="html.parser")
            tables = soup.findAll("table")
            version = tables[0].find_all("tr")[0].find_all("td")[1].text
        return version



