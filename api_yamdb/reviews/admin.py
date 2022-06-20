from django.contrib import admin

from .models import Categories, Comments, Genres, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('pk', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('pk', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    list_display_links = ('pk', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Comments)
admin.site.register(Review)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Genres, GenreAdmin)
admin.site.register(Title, TitleAdmin)
