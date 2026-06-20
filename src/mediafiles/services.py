# mediafiles/services.py

from .models import MediaLink


def attach_media(media_file, entity_type, entity_id):
    return MediaLink.objects.create(
        media_file=media_file,
        entity_type=entity_type,
        entity_id=entity_id,
    )

def get_entity_media(entity_type, entity_id):
    return MediaFile.objects.filter(
        links__entity_type=entity_type,
        links__entity_id=entity_id,
    )