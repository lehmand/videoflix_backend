from django.contrib import admin
from .models import Video
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

class VideoResources(resources.ModelResource):
    """
    Resource class for the Video model that enables import/export functionality.
    
    This class defines how Video model instances can be imported from or exported to
    various formats (CSV, XLS, JSON, etc.) using the django-import-export library.
    It provides a framework for field mapping and data handling during import/export operations.
    """
    class Meta:
        model = Video


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    """
    Admin configuration for the Video model.
    
    Extends ImportExportModelAdmin to provide import/export functionality in the Django admin.
    This allows administrators to:
    - Import videos in bulk from spreadsheets or other data formats
    - Export existing videos to various formats for backup or analysis
    - Manage video entries through a customized admin interface
    
    The resource_classes attribute specifies which resource class(es) should be used
    for import/export operations.
    """
    resource_classes = [VideoResources]