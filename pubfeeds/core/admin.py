from django.contrib import admin
from .models import Feed, Section, Edition, Article, PublishingSchedule

class SectionInline(admin.StackedInline):
    model = Section

class ScheduleInline(admin.StackedInline):
    model = PublishingSchedule

class FeedAdmin(admin.ModelAdmin):
    inlines = [SectionInline, ScheduleInline]

admin.site.register(Feed, FeedAdmin)

class ArticleInline(admin.StackedInline):
    model = Article

class EditionAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]

admin.site.register(Edition, EditionAdmin)