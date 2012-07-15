import math

from django.test import TestCase
from django.utils import simplejson as json

from pubmed_search.models import Article, Author, Frequency, Journal, Order, Term
from pubmed_search.nlp import clean_term, tfidf
from pubmed_search.utils import create_db_entries
from pubmed_search.views import autosearch, search


# Test pubmed_search.utils, .nlp and .views
class ArticleBaseTest(TestCase):
    def setUp(self):
        self.raw_record = r"""[
    {
        "abstract": "Current practices of reporting critical laboratory values make it challenging to measure and assess the timeliness of receipt by the treating physician as required by The Joint Commission's 2008 National Patient Safety Goals.\nA multidisciplinary team of laboratorians, clinicians, and information technology experts developed an electronic ALERTS system that reports critical values via the laboratory and hospital information systems to alphanumeric pagers of clinicians and ensures failsafe notification, instant documentation, automatic tracking, escalation, and reporting of critical value alerts. A method for automated acknowledgment of message receipt was incorporated into the system design.\nThe ALERTS system has been applied to inpatients and eliminated approximately 9000 phone calls a year made by medical technologists. Although a small number of phone calls were still made as a result of pages not acknowledged by clinicians within 10 min, they were made by telephone operators, who either contacted the same physician who was initially paged by the automated system or identified and contacted alternate physicians or the patient's nurse. Overall, documentation of physician acknowledgment of receipt in the electronic medical record increased to 95% of critical values over 9 months, while the median time decreased to <3 min.\nWe improved laboratory efficiency and physician communication by developing an electronic system for reporting of critical values that is in compliance with The Joint Commission's goals.",
        "authors": [
            "Parl FF",
            "O'Leary MF",
            "Kaiser AB",
            "Paulett JM",
            "Statnikova K",
            "Shultz EK"
        ],
        "journal": "Clin. Chem.",
        "pubmedUrl": "http://www.ncbi.nlm.nih.gov/pubmed/20040617",
        "title": "Implementation of a closed-loop reporting system for critical values and clinical communication in compliance with goals of the joint commission."
    }]"""
        self.records = json.loads(self.raw_record)

class EntriesTest(ArticleBaseTest):
    def test_create_db_entries(self):
        record = self.records[0]
        create_db_entries(record)
        articles = Article.objects.all()
        self.assertEqual(1, articles.count())
        article = articles[0]
        self.assertEqual(record['title'], article.title)
        self.assertEqual(record['abstract'], article.abstract)
        self.assertEqual(record['pubmedUrl'], article.pubmed_url)
        authors = article.authors.all()
        for author in authors:
            name = author.__unicode__()
            self.assertIn(name, record["authors"])

class TermsTest(ArticleBaseTest):
    def test_create_term_frequencies(self):
        record = self.records[0]
        create_db_entries(record)
        implementation = Term.objects.get(term='implementation')
        impl_freq = Frequency.objects.get(term=implementation)
        self.assertEqual(1, impl_freq.frequency)

class CleanTermTest(TestCase):
    def test_clean_term(self):
        words = ('Clin.', 'Chem.', 'Implementation', 'closed-loop', 'commission.')
        cleaned_words = [clean_term(word) for word in words]
        self.assertIn('clin', cleaned_words)
        self.assertIn('chem', cleaned_words)
        self.assertIn('implementation', cleaned_words)
        self.assertIn('closed-loop', cleaned_words)
        self.assertIn('commission', cleaned_words)

class TFIDFTest(ArticleBaseTest):
    def test_tfidf(self):
        record = self.records[0]
        create_db_entries(record)
        articles = Article.objects.all()
        article = articles[0]
        implementation = Term.objects.get(term='implementation')

        idf = math.log(1.0/2.0)

        self.assertEqual(idf, tfidf(implementation, article))

class AutosearchTest(ArticleBaseTest):
    def test_autosearch(self):
        record = self.records[0]
        create_db_entries(record)
        response = self.client.get('/autosearch/?q=implementation')
        self.assertContains(response, 'Implementation', count=1)
        self.assertTemplateNotUsed(response, 'pubmed_search/article_list.html')
        self.assertTemplateNotUsed(response, 'pubmed_search/article_detail.html')
        self.assertTemplateNotUsed(response, 'pubmed_search/search.html')

class SearchTest(ArticleBaseTest):
    def test_search(self):
        record = self.records[0]
        create_db_entries(record)
        response = self.client.post('/', {'q': 'implementation'})
        self.assertTemplateUsed(response, 'pubmed_search/search.html')
        self.assertContains(response, 'Implementation', count=1)
        self.assertEqual(1, len(response.context['articles']))
        self.assertEqual('implementation', response.context['query_terms'][0])
        self.assertEqual(1, response.context['total_documents'])

