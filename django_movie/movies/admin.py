from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """Форма для редактирования текста в поле Movie.description редактором CKEditor"""
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)

class ReviewInline(admin.TabularInline):
    model = Review
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")
    extra = 1

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = "Кадр из фильма"

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    list_display = ("title", "movie")
    readonly_fields = ("get_image",)
    extra = 1

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="100">')

    get_image.short_description = "Кадр из фильма"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    # list_editable = ()
    actions = ("publish", "unpublish")

    # форма с редактором
    form = MovieAdminForm

    search_fields = ("title", "category__name")
    inlines = (ReviewInline, MovieShotsInline)
    save_on_top = True
    save_as = True
    readonly_fields = ("get_image", )
    # fields = (("actors", "directors", "genres"), )
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), )
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse", ),
            "fields": (("actors", "directors", "genres"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Опции", {
            "fields": (("url", "draft"),)
        }),
    )

    # actions для админки
    def publish(self, request, queryset):
        self._set_queryset_publish(request, queryset, False)

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ("change", )

    def unpublish(self, request, queryset):
        self._set_queryset_publish(request, queryset, True)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ("change",)

    def _set_queryset_publish(self, request, queryset, flag: bool):
        """Публикование/ снятие с публикации записей"""
        row_update = queryset.update(draft=flag)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f"{row_update} записей обновлены"

        self.message_user(request, f"{message_bit}")

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110">')

    get_image.short_description = "Постер"

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("ip", "star", "movie")

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
