from django.contrib import admin
from .models import Video
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

class VideoResources(resources.ModelResource):

    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    resource_classes = [VideoResources]
