def delete_infraction_event_video_clip(sender, instance, using, **kwargs):
    if instance and instance.infraction_video:
        instance.infraction_video.delete()
