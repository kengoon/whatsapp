from typing import Union
from whatsapp.errors import Handle
from whatsapp.models import Message, WhatsappConfig, MessageResponse, MessageTypeProperties, Location
import requests


class WhatsAppMessage:
    def __init__(self, config: WhatsappConfig):
        self.config = config
        self.url = "/messages"

    def reply_text(
            self,
            to: str,
            body: str,
            message_id: str,
            recipient_type: str = "individual",
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            context=MessageTypeProperties(message_id=message_id),
            type="text",
            text=MessageTypeProperties(body=body),
        )
        return self.send_message(message)

    def mark_as_read(self, message_id: str) -> MessageResponse:
        message = Message(
            status="read",
            message_id=message_id,
        )
        return self.send_message(message)

    def send_text(
            self,
            to: str,
            body: str,
            recipient_type: str = "individual",
            preview_url: bool = True
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="text",
            text=MessageTypeProperties(preview_url=preview_url, body=body),
        )
        return self.send_message(message)

    def send_video(
            self,
            to: str,
            media_id: str,
            caption: str = None,
            recipient_type: str = "individual",
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="video",
            video=MessageTypeProperties(id=media_id, caption=caption)
        )
        return self.send_message(message)

    def send_image(
            self,
            to: str,
            media_id: str,
            caption: str = None,
            recipient_type: str = "individual",
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="image",
            video=MessageTypeProperties(id=media_id, caption=caption)
        )
        return self.send_message(message)

    def send_audio(
            self,
            to: str,
            media_id: str,
            recipient_type: str = "individual",
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="image",
            video=MessageTypeProperties(id=media_id)
        )
        return self.send_message(message)

    def send_document(
            self,
            to: str,
            media_id: str,
            caption: str = None,
            filename: str = None,
            recipient_type: str = "individual",
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="document",
            video=MessageTypeProperties(id=media_id, caption=caption, filename=filename)
        )
        return self.send_message(message)

    def send_sticker(
            self,
            to: str,
            sticker_id: str,
            recipient_type: str = "individual",
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="sticker",
            sticker=MessageTypeProperties(id=sticker_id)
        )
        return self.send_message(message)

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
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="location",
            location=Location(latitude=latitude, longitude=longitude, name=name, address=address)
        )
        return self.send_message(message)

    def react(
            self,
            to: str,
            message_id: str,
            emoji: str = None,
            recipient_type: str = "individual",
    ) -> MessageResponse:
        message = Message(
            recipient_type=recipient_type,
            to=to,
            type="reaction",
            reaction=MessageTypeProperties(message_id=message_id, emoji=emoji),
        )
        return self.send_message(message)

    def send_message(self, data: Union[dict[str, str], Message]) -> MessageResponse:
        if isinstance(data, Message):
            data = data.model_dump(exclude_none=True)
        r = requests.post(
            f"{self.config.api_url}/messages",
            headers=self.config.headers | {"Content-Type": "application/json"},
            json=data
        )
        if r.status_code != 200:
            Handle(r.json())
        return MessageResponse(**r.json())
