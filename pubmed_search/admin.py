from django.contrib import admin
from author_tfidf.pubmed_search.models import (Article,
                                                         Author,
                                                         Journal,
                                                         Term,
                                                         Frequency,
                                                         Order)


class OrderInline(admin.TabularInline):
    model = Order
    ordering = ["order", ]
    extra=0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [OrderInline, ]
    filter_horizontal = ["authors"]
    search_fields = ["title",
                     "abstract",
                     "authors__last_name",
                     "journal__name"]


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["last_name", ]


class JournalAdmin(admin.ModelAdmin):
    search_fields = ["name", ]


class FrequencyInline(admin.TabularInline):
    model = Frequency
    ordering = ["-frequency", ]
    readonly_fields = ["frequency", "article"]
    extra = 0


class TermAdmin(admin.ModelAdmin):
    inlines = [FrequencyInline, ]
    search_fields = ["term", ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Frequency)
