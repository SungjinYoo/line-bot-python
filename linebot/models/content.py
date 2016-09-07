from abc import ABCMeta


class NoContentMappingException(Exception):
    """
    no content type matched in mapping table
    """


class ContentType:
    TEXT = 1
    IMAGE = 2
    VIDEO = 3
    AUDIO = 4
    LOCATION = 7
    STICKER = 8
    CONTACT = 10
    RICH_MESSAGE = 12


class Content(metaclass=ABCMeta):
    def __init__(self, content):
        self.id_ = content['id']
        self.from_ = content['from']
        self.content_type = content['contentType']
        self.to_type = content['toType']


class TextContent(Content):
    def __init__(self, content):
        super().__init__(content)
        self.text = content['text']


class ImageContent(Content):
    def __init__(self, content):
        super().__init__(content)
        self.original_content_url = content['originalContentUrl']
        self.preview_image_url = content['previewImageUrl']


class VideoContent(Content):
    def __init__(self, content):
        super().__init__(content)
        self.original_content_url = content['originalContentUrl']
        self.preview_image_url = content['previewImageUrl']


class AudioContent(Content):
    def __init__(self, content):
        super().__init__(content)
        self.original_content_url = content['originalContentUrl']
        # TODO: metadata = {AUDLEN}
        self.content_metadata = content['contentMetadata']


class LocationContent(Content):
    def __init__(self, content):
        super().__init__(content)
        self.text = content['text']
        # TODO: location = {title, address, latitude, longitude}
        self.location = content['location']


class StickerContent(Content):
    def __init__(self, content):
        super().__init__(content)
        # TODO: metadata = {STKPKGID, STKID, STKVER, STKTXT}
        self.content_metadata = content['contentMetadata']


class ContactContent(Content):
    def __init__(self, content):
        super().__init__(content)
        # TODO: metadata = {mid, displayName}
        self.content_metadata = content['contentMetadata']


class RichMessageContent(Content):
    def __init__(self, content):
        super().__init__(content)
        # TODO: metadata = {DOWNLOAD_URL, SPEC_REV, ALT_TEXT, MARKUP_JSON(1)}
        self.content_metadata = {}


class ContentMapper:
    CONTENT_MAPPING = {
        ContentType.TEXT: TextContent,
        ContentType.IMAGE: ImageContent,
        ContentType.VIDEO: VideoContent,
        ContentType.AUDIO: AudioContent,
        ContentType.LOCATION: LocationContent,
        ContentType.STICKER: StickerContent,
        ContentType.CONTACT: ContactContent,
        ContentType.RICH_MESSAGE: RichMessageContent,
    }

    @classmethod
    def map(cls, content):
        class_ = cls.CONTENT_MAPPING.get(content['contentType'])
        if not class_:
            raise NoContentMappingException()

        return class_(content)