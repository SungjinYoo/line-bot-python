from linebot.models.content import ContentType


def create_text(text):
    return {
        'contentType': ContentType.TEXT,
        'text': text,
    }


def create_image(image_url, preview_image_url):
    return {
        'contentType': ContentType.IMAGE,
        'originalContentUrl': image_url,
        'previewImageUrl': preview_image_url,
    }


def create_video(video_url, preview_image_url):
    return {
        'contentType': ContentType.VIDEO,
        'originalContentUrl': video_url,
        'previewImageUrl': preview_image_url,
    }


def create_audio(audio_url, length):
    return {
        'contentType': ContentType.AUDIO,
        'originalContentUrl': audio_url,
        'contentMetadata': {
            'AUDLEN': length if isinstance(length, str) else str(length)
        }
    }


def create_location(text, latitude, longitude):
    return {
        'contentType': ContentType.LOCATION,
        'text': text,
        'location': {
            'title': text,
            'latitude': latitude,
            'longitude': longitude,
        }
    }


def create_sticker(stkid, stkpkgid, stkver=None):
    metadata = {
        'STKID': str(stkid),
        'STKPKGID': str(stkpkgid),
    }
    if stkver:
        metadata['STKVER'] = str(stkver)

    return {
        'contentType': ContentType.STICKER,
        'contentMetadata': metadata,
    }