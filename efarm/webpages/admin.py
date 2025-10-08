from django.contrib import admin
from .models import OurTeam, LatestBlog, HomeSlider
from django.utils.html import format_html

# Register your models here.
class OurTeamAdmin(admin.ModelAdmin):

    # Properties 
    def myphoto(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.your_photo.url))

    # Overwriting the list.
    list_display = ('id', 'myphoto', 'first_name', 'designation', 'created_date')
    list_display_links = ('first_name', 'id')
    search_fields = ('first_name', )
    list_filter = ('first_name', )

class LatestBlogAdmin(admin.ModelAdmin):

    # Properties 
    def myphoto(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    # Overwriting the list.
    list_display = ('id', 'myphoto', 'title', 'created_date')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'created_date', )
    list_filter = ('title', 'created_date', )

class HomeSliderAdmin(admin.ModelAdmin):

    # Properties 
    def myphoto(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    # Overwriting the list.
    list_display = ('id', 'myphoto', 'title', 'created_date')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'created_date', )
    list_filter = ('title', 'created_date', )

admin.site.register(OurTeam, OurTeamAdmin)
admin.site.register(LatestBlog, LatestBlogAdmin)
admin.site.register(HomeSlider, HomeSliderAdmin)