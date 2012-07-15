from math import fsum

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson as json
from django.views.decorators.http import require_http_methods, require_GET

from pubmed_search.forms import SearchForm
from pubmed_search.models import Article, Author, Term
from pubmed_search.nlp import tfidf


def _deduplicate_articles(articles):
    """Given a sequence of (TF-IDF, article) tuples, remove duplicate articles
    from the list, and remove the TF-IDF score. Returns a list of articles."""
    visited = []
    for item in articles:
        if item[1] in visited:
            continue
        else:
            visited.append(item[1])
    return visited


def _find_articles(query_terms):
    """Given a list of query terms, find all articles that contain those
    terms."""
    q = Q()
    for term in query_terms:
        #q = q | Q(frequency__term__term__icontains=term)
        q = q | Q(frequency__term__term__iexact=term)
    articles = Article.objects.filter(q).distinct()
    return articles


@require_GET
def autosearch(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query_terms = form.cleaned_data['q'].split()
        results = _find_articles(query_terms)

        c = []
        for article in results:
            c.append({"pk":article.pk, "title":article.title, "url":article.get_absolute_url()})
        content = json.dumps(c)
        return HttpResponse(content, content_type='application/json')


@require_http_methods(["GET", "POST"])
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query_terms = form.cleaned_data['q'].split()
            query_terms = [term.lower() for term in query_terms]
            intermediate_results = _find_articles(query_terms)

            # calculate the TF-IDF of each term per document,
            # order results by TF-IDF
            terms = Term.objects.filter(term__in=query_terms)
            ordered_results = []
            for term in terms:
                for doc in intermediate_results:
                    ordered_results.append((tfidf(term, doc), doc))
            ordered_results.sort(reverse=True)

            # strip out duplicate articles without changing the order
            results = _deduplicate_articles(ordered_results)

            # calculate total number of articles for "X of Y documents"
            total_docs = Article.objects.count()

            # Calculate the average TF-IDF for each author in search results.
            # Average TF-IDF includes scores of zero for documents that match
            # term A, but not term B. That is, a doc that matches A will have a
            # TF-IDF of some positive float, but if that same doc does *not*
            # match term B, it will have a TF-IDF of 0 for term B.
            # ordered_results has a list of (TF-IDF, article) tuples of all
            # results, so start with that and create a dictionary with authors
            # as keys and lists of (TF-IDF, article) tuples as values.
            author_totals = {}
            for score, doc in ordered_results:
                for author in doc.authors.all():
                    scores = author_totals.setdefault(author.pk, [])
                    scores.append(score)

            # average the scores per author
            author_averages = []
            total_results = len(ordered_results)
            for author_pk, scores in author_totals.items():
                scores_sum = fsum(scores)
                average = scores_sum / total_results
                author = Author.objects.get(pk=author_pk)
                author_averages.append((author, average))


            return render(request, 'pubmed_search/search.html', {'articles': results,
                                                                 'query_terms': query_terms,
                                                                 'total_documents': total_docs,
                                                                 'author_averages': author_averages})
        else:
            return render(request, 'pubmed_search/search.html', {'query_terms': request.POST})
    else:
        return render(request, 'pubmed_search/search.html')
