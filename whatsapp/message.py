from typing import Union
from whatsapp.errors import Handle
from whatsapp.model import Message, WhatsappConfig, MessageResponse, MessageTypeProperties, Location
from bs4 import BeautifulSoup
import requests


class WhatsAppMessage:
    def __init__(self, config: WhatsappConfig):
        self.config = config
        self._init_api_version()
        self.url = f"https://graph.facebook.com/{self.version}/{self.config.phone_number_id}/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.token}",
        }

    def _init_api_version(self):
        if self.config.version == "latest":
            r = requests.get("https://developers.facebook.com/docs/graph-api/changelog/")
            soup = BeautifulSoup(r.text, features="html.parser")
            tables = soup.findAll("table")
            version = tables[0].find_all("tr")[0].find_all("td")[1].text
            self.version = version
        else:
            self.version = self.config.version

    def reply_text(
            self,
            to: str,
            body: str,
            message_id: str,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            context=MessageTypeProperties(message_id=message_id),
            type="text",
            text=MessageTypeProperties(body=body),
        )
        self.send_message(message)

    def mark_as_read(self, message_id: str):
        message = Message(
            status="read",
            message_id=message_id,
        )
        self.send_message(message)

    def send_text(
            self,
            to: str,
            body: str,
            recipient_type: str = "individual",
            preview_url: bool = True
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="text",
            text=MessageTypeProperties(preview_url=preview_url, body=body),
        )
        self.send_message(message)

    def send_video(
            self,
            to: str,
            media_id: str,
            caption: str = None,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="video",
            video=MessageTypeProperties(id=media_id, caption=caption)
        )
        self.send_message(message)

    def send_image(
            self,
            to: str,
            media_id: str,
            caption: str = None,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="image",
            video=MessageTypeProperties(id=media_id, caption=caption)
        )
        self.send_message(message)

    def send_audio(
            self,
            to: str,
            media_id: str,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="image",
            video=MessageTypeProperties(id=media_id)
        )
        self.send_message(message)

    def send_document(
            self,
            to: str,
            media_id: str,
            caption: str = None,
            filename: str = None,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="document",
            video=MessageTypeProperties(id=media_id, caption=caption, filename=filename)
        )
        self.send_message(message)

    def send_sticker(
            self,
            to: str,
            sticker_id: str,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="sticker",
            sticker=MessageTypeProperties(id=sticker_id)
        )
        self.send_message(message)

    def send_contact(self, message: Message):
        pass

    def send_location(
            self,
            to: str,
            latitude: str,
            longitude: str,
            name: str = None,
            address: str = None,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="location",
            location=Location(latitude=latitude, longitude=longitude, name=name, address=address)
        )
        self.send_message(message)

    def react(
            self,
            to: str,
            message_id: str,
            emoji: str = None,
            recipient_type: str = "individual",
    ):
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="reaction",
            reaction=MessageTypeProperties(message_id=message_id, emoji=emoji),
        )
        self.send_message(message)

    def send_message(self, data: Union[dict[str, str], Message]) -> MessageResponse:
        if isinstance(data, Message):
            data = data.model_dump(exclude_none=True)
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            return MessageResponse(**r.json())
        Handle(r.json())



WhatsAppMessage(WhatsappConfig(token="djd", verify_token="latest", phone_number_id="dkdkdk")).reply_text(context={"message_id": "nwa"}, to="3838383838", text={"body": "ddkdkdd"})