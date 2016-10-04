def create_text(text):
    return {
        "type": "text",
        "text": text,
    }


def create_image(image_url, preview_image_url):
    return {
        "type": "image",
        "originalContentUrl": image_url,
        "previewImageUrl": preview_image_url,
    }


def create_video(video_url, preview_image_url):
    return {
        "type": "video",
        "originalContentUrl": video_url,
        "previewImageUrl": preview_image_url,
    }


def create_audio(audio_url, length):
    return {
        "type": "audio",
        "originalContentUrl": audio_url,
        "duration": length,
    }


def create_location(title, address, latitude, longitude):
    return {
        "type": "location",
        "title": title,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
    }


def create_sticker(package_id, sticker_id):
    return {
        "type": "sticker",
        "packageId": package_id,
        "stickerId": sticker_id,
    }