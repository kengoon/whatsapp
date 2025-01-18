from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, EmailStr, field_validator


class WhatsappConfig(BaseModel):
    token: str = Field(description="Token for WhatsApp cloud API")
    phone_number_id: str = Field(description="phone numbers ID")
    verify_token: str = Field(description="Your whatsapp api verify token")
    version: str = Field(default="latest", description="Whatsapp API version")


class MessageResponseContact(BaseModel):
    input: str
    wa_id: str


class MessageResponseMessage(BaseModel):
    id: str


class MessageResponse(BaseModel):
    messaging_product: Optional[str] = Field(default=None)
    contacts: Optional[MessageResponseContact] = Field(default=None)
    messages: Optional[MessageResponseMessage] = Field(default=None)
    success: Optional[bool] = Field(default=None)


class ContactAddress(BaseModel):
    street: Optional[str] = Field(description="Street address of the contact")
    city: Optional[str] = Field(description="City where the contact resides")
    state: Optional[str] = Field(description="Two-letter state code")
    zip: Optional[str] = Field(description="Postal or ZIP code.")
    country: Optional[str] = Field(description="Country name")
    country_code: Optional[str] = Field(description="ISO two-letter country code")
    type: Optional[str] = Field(description="Type of address, such as home or work")


class ContactEmail(BaseModel):
    email: Optional[EmailStr] = Field(description="Email address of the contact")
    type: Optional[str] = Field(description="Type of email, such as home or work")


class ContactName(BaseModel):
    formated_name: str = Field(
        description="Contact's formatted name. This will appear in the message alongside the profile arrow button")
    first_name: Optional[str] = Field(description="Contact's first name.")
    last_name: Optional[str] = Field(description="Contact's last name.")
    middle_name: Optional[str] = Field(description="Contact's middle name.")
    suffix: Optional[str] = Field(description="Suffix for the contact's name, if applicable, such as Esq., etc.")
    prefix: Optional[str] = Field(description="Prefix for the contact's name, such as Mr., Ms., Dr., etc.")


class ContactOrganization(BaseModel):
    company: Optional[str] = Field(description="Name of the company where the contact works")
    department: Optional[str] = Field(description="Department within the company")
    title: Optional[str] = Field(description="Contact's job title.")


class ContactPhone(BaseModel):
    phone: Optional[str] = Field(description="WhatsApp user phone number.")
    type: Optional[str] = Field(
        description="Type of phone number. For example, cell, mobile, main, iPhone, home, work, etc.")
    wa_id: Optional[str] = Field(
        description="WhatsApp user ID. If omitted, the message will display an "
                    "Invite to WhatsApp button instead of the standard buttons."
    )


class ContactUrl(BaseModel):
    url: Optional[str] = Field(description="Website URL associated with the contact or their company")
    type: Optional[str] = Field(
        description="Type of website. For example, company, work, personal, Facebook Page, Instagram, etc.")


class Contact(BaseModel):
    addresses: Optional[list[ContactAddress]] = Field(description="Whatsapp contact address")
    birthday: Optional[str] = Field(description="Contact's birthday in YYYY-MM-DD format.")
    emails: Optional[list[ContactEmail]] = Field(description="Email address of the contact")
    name: ContactName = Field(description="Contact's name.")
    org: Optional[ContactOrganization] = Field(description="Contact's organization.")
    phones: Optional[list[ContactPhone]] = Field(description="Contact's phone number.")
    urls: Optional[list[ContactUrl]] = Field(description="Website URL associated with the contact or their company")

    @field_validator("birthday")
    def birthday_yyyy_mm_dd_validator(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError("birthday data does not match the format 'YYYY-MM-DD'")
        return value


class Location(BaseModel):
    latitude: str = Field(description="Location latitude in decimal degrees")
    longitude: str = Field(description="Location longitude in decimal degrees")
    name: Optional[str] = Field(description="Location name")
    address: Optional[str] = Field(description="Location address")


class MessageTypeProperties(BaseModel):
    id: Optional[str] = Field(default=None, description="Whatsapp media ID")
    caption: Optional[str] = Field(default=None, description="Whatsapp media caption")
    filename: Optional[str] = Field(default=None, description="Whatsapp media filename")
    body: Optional[str] = Field(default=None, description="Whatsapp message body")
    preview_url: Optional[bool] = Field(default=None, description="Whatsapp media preview url")
    message_id: Optional[str] = Field(default=None, description="Whatsapp message ID")
    emoji: Optional[str] = Field(default=None, description="Whatsapp emoji reaction")


class InteractiveAction(BaseModel):
    name: Optional[str] = Field(default=None, description="Whatsapp interactive action name")


class InteractiveMessage(BaseModel):
    type: Optional[str] = Field(
        default=None,
        description="Whatsapp interactive header type",
        examples=["image", "video", "text", "document"]
    )
    text: str = Field(description="Whatsapp interactive text")
    image: Optional[dict[str, str]] = Field(default=None, description="Whatsapp interactive image")


class Interactive(BaseModel):
    type: str = Field(
        description="Whatsapp interactive mode",
        examples=["list", "cta_url", "flow", "button", "location_request_message"]
    )
    header: Optional[InteractiveMessage] = Field(
        description="Header content. Supports the following types: document, image, text, video")
    body: InteractiveMessage = Field(description="Message body text.")
    footer: InteractiveMessage = Field(description="Message footer text.")

    @field_validator("footer", "body")
    def exclude_fields(cls, value: InteractiveMessage) -> InteractiveMessage:
        if value.type is not None or value.image is not None:
            raise ValueError(f"{value} ust only contain text, not type or image")
        return value


class Message(BaseModel):
    messaging_product: str = Field(default="whatsapp", description="Whatsapp messaging product", examples=["whatsapp"])
    status: Optional[str] = Field(default=None, description="Whatsapp messaging status")
    message_id: Optional[str] = Field(default=None, description="Whatsapp messaging ID")
    content: Optional[str] = Field(default=None, description="Message content")
    to: Optional[str] = Field(default=None, description="Message to")
    type: Optional[str] = Field(
        default=None,
        description="Message type",
        examples=["text", "image", "video", "text", "document", "sticker", "reaction", "contact", "location"]
    )
    recipient_type: Optional[str] = Field(default=None, description="Message recipient type")
    sender: Optional[str] = Field(default=None, description="Message sender")
    text: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message text")
    audio: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message audio")
    video: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message video")
    image: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message image")
    sticker: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message sticker")
    document: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message document")
    reaction: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message reaction")
    context: Optional[MessageTypeProperties] = Field(default=None, description="Whatsapp message reply context")
    contact: Optional[list[Contact]] = Field(default=None, description="Whatsapp contact list")
    location: Optional[Location] = Field(default=None, description="Whatsapp message location")

