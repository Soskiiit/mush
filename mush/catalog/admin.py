from django.contrib import admin

from .models import Photo, Project


class PhotoTabular(admin.TabularInline):
    extra = 0
    model = Photo
    readonly_fields = ('img_thmb',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (PhotoTabular,)


admin.site.register(Photo)
