def deleteInfractionEventVideoClip(sender, instance, using, **kwargs):
    if instance and instance.infraction_video:
        instance.infraction_video.delete()
