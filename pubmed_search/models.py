from django.db import models


class Journal(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name", ]

    def __unicode__(self):
        return self.name


class Author(models.Model):
    initials = models.CharField("initials of given name(s)", max_length=10)
    last_name = models.CharField(max_length=255, db_index=True)

    class Meta:
        ordering = ["last_name", "initials"]

    def __unicode__(self):
        return u"%s %s" % (self.last_name, self.initials)


class Article(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField(blank=True)
    pubmed_url = models.URLField("PubMed URL", max_length=255)
    journal = models.ForeignKey(Journal)
    authors = models.ManyToManyField(Author, through='Order')

    class Meta:
        ordering = ["title", ]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', [str(self.pk)])


class Order(models.Model):
    author = models.ForeignKey(Author)
    article = models.ForeignKey(Article)
    order = models.IntegerField(max_length=10)

    class Meta:
        ordering = ['article', 'order']

    def __unicode__(self):
        return u"%s: %s for %s" % (self.author, self.order, self.article)


class Term(models.Model):
    term = models.CharField(max_length=255, unique=True)
    documents = models.ManyToManyField(Article, through='Frequency')

    class Meta:
        ordering = ["term", ]

    def __unicode__(self):
        return self.term


class Frequency(models.Model):
    term = models.ForeignKey(Term)
    article = models.ForeignKey(Article)
    frequency = models.IntegerField(max_length=255)

    class Meta:
        ordering = ["term", ]
        verbose_name_plural = "frequencies"

    def __unicode__(self):
        return u"%s: %s for %s" % (self.term, self.frequency, self.article)
