import math

from django.conf import settings

from pubmed_search.models import Article, Frequency


def clean_term(raw_term, acceptable=settings.ACCEPTABLE_CHARACTERS):
    """Return a normalized version of raw_term. By default, strips all
    punctuation except hyphens and lowercases the term.

    """
    characters = [char for char in raw_term if char in acceptable]
    cleaned_term = ''.join(characters).lower()
    return cleaned_term


def tfidf(term, article):
    try:
        frequency = Frequency.objects.get(term=term, article=article)
        tf = frequency.frequency

        total_documents = Article.objects.count()
        term_appearance = Frequency.objects.filter(term=term).count()

        idf = math.log(total_documents / (1.0 + term_appearance))

        return tf*idf

    except Frequency.DoesNotExist:
        return 0
