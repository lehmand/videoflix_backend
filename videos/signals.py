from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .tasks import convert_video, convert_video_hls
import os
# import django_rq



@receiver(post_save, sender=Video)
def video_post_save(instance, created, **kwargs):
    if created:
        # queue = django_rq.get_queue('default', autocommit=True)
        # queue.enqueue(convert_video, instance.file.path, 'hd480', '480p')
        # queue.enqueue(convert_video, instance.file.path, 'hd720', '720p')
        # queue.enqueue(convert_video_hls, instance.file.path, 'hd480', '480p')
        # queue.enqueue(convert_video_hls, instance.file.path, 'hd720', '720p')

        convert_video(instance.file.path, 'hd480', '480p')
        convert_video(instance.file.path, 'hd720', '720p')



@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

    base, ext = os.path.splitext(instance.file.path)
    converted_files = [base + '_480p.mp4', base + '_720p.mp4']
    for file_path in converted_files:
        if os.path.isfile(file_path):
            os.remove(file_path)
  
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)