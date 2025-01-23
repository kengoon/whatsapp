# Whatsapp
**whatsapp** is an unofficial open-source Python library designed to interact with the WhatsApp Cloud API,
allowing developers to send and receive messages, manage media, and handle interactive messages programmatically.
This library aims to simplify integration with WhatsApp's business solutions, providing an easy-to-use interface for
various WhatsApp functionalities.

### To SEND message

```python
from whatsapp import WhatsApp

whatsapp = WhatsApp(
    token="<YOUR-WHATSAPP-TOKEN>",
    verify_token="<YOUR-WHATSAPP-VERIFY-WEBHOOK-TOKEN>",
    phone_number_id="<YOUR-WHATSAPP-PHONE_NUMBER_ID>"
)

response = whatsapp.message.send_text(to="+1234567890", body="hi, welcome to my business")
```

### To REPLY message

```python
from whatsapp import WhatsApp

whatsapp = WhatsApp(
    token="<YOUR-WHATSAPP-TOKEN>",
    verify_token="<YOUR-WHATSAPP-VERIFY-WEBHOOK-TOKEN>",
    phone_number_id="<YOUR-WHATSAPP-PHONE_NUMBER_ID>"
)

response = whatsapp.message.reply_text(
    to="+1234567890",
    body="hi, welcome to my business",
    message_id="<MESSAGE_ID_TO_REPLY>"
)
```

### To mark message as READ

```python
from whatsapp import WhatsApp

whatsapp = WhatsApp(
    token="<YOUR-WHATSAPP-TOKEN>",
    verify_token="<YOUR-WHATSAPP-VERIFY-WEBHOOK-TOKEN>",
    phone_number_id="<YOUR-WHATSAPP-PHONE_NUMBER_ID>"
)

response = whatsapp.message.mark_as_read(message_id="<MESSAGE_ID-TO-MARK-AS-READ>")
```

### To REACT to a message

```python
from whatsapp import WhatsApp

whatsapp = WhatsApp(
    token="<YOUR-WHATSAPP-TOKEN>",
    verify_token="<YOUR-WHATSAPP-VERIFY-WEBHOOK-TOKEN>",
    phone_number_id="<YOUR-WHATSAPP-PHONE_NUMBER_ID>"
)
response = whatsapp.message.react(
    to="+1234567890",
    message_id="<MESSAGE_ID-TO-REACT>",
    emoji="\uD83D\uDE00"  # EMOJI Unicode 
)
```

### To send LOCATION

```python
from whatsapp import WhatsApp

whatsapp = WhatsApp(
    token="<YOUR-WHATSAPP-TOKEN>",
    verify_token="<YOUR-WHATSAPP-VERIFY-WEBHOOK-TOKEN>",
    phone_number_id="<YOUR-WHATSAPP-PHONE_NUMBER_ID>"
)
response = whatsapp.message.send_location(
    to="+1234567890",
    latitude="9.0820",
    longitude="8.6753",
    name="<LOCATION-NAME>",
    address="<LOCATION-ADDRESS>"
)
```

### To Send VIDEO, AUDIO, DOCUMENT, IMAGE

```python
from whatsapp import WhatsApp

whatsapp = WhatsApp(
    token="<YOUR-WHATSAPP-TOKEN>",
    verify_token="<YOUR-WHATSAPP-VERIFY-WEBHOOK-TOKEN>",
    phone_number_id="<YOUR-WHATSAPP-PHONE_NUMBER_ID>"
)

audio_response = whatsapp.message.send_audio(
    to="+1234567890",
    media_id="<MESSAGE_ID-TO-SEND_AUDIO>"
)

video_response = whatsapp.message.send_video(
    to="+1234567890",
    media_id="<MESSAGE_ID-TO-SEND_VIDEO>",
    caption="Checkout this product video"
)

image_response = whatsapp.message.send_image(
    to="+1234567890",
    media_id="<MESSAGE_ID-TO-SEND_IMAGE>",
    caption="Checkout this product image"
)
```

### To UPLOAD, QUERY AND DOWNLOAD media

```python
from whatsapp import WhatsApp

whatsapp = WhatsApp(
    token="<YOUR-WHATSAPP-TOKEN>",
    verify_token="<YOUR-WHATSAPP-VERIFY-WEBHOOK-TOKEN>",
    phone_number_id="<YOUR-WHATSAPP-PHONE_NUMBER_ID>"
)

# upload media
media = whatsapp.media.upload_media("/path/to/file")

# query media
media_query = whatsapp.media.query_media_url(media.id)

# download media
whatsapp.media.download_media(media_query.url)

# if you want to save the media file yourself:

file_content, filename = whatsapp.media.download_media(media_query.url)

with open(f"/path/to/{filename}", "w") as f:
    f.write(file_content)
```