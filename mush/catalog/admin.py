from catalog.models import Photo, Model3D, Project
from django.contrib import admin


class PhotoTabular(admin.TabularInline):
    extra = 0
    model = Photo
    readonly_fields = ('img_thmb',)


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    inlines = (PhotoTabular,)


admin.site.register(Photo)
admin.site.register(Project)
