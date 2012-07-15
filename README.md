Author TD-IDF Calculator
========================

Requirements
============
I built this project to explore a basic part of natural language processing,
calculating relevance of an article and an author for a given keyword search
term. This project, in addition to the search functionality, also includes
an import tool, a view providing a dynamic-result search page, and a chart of
author's average TF-IDF. To write the app, I used Django, jQuery, Flot and
HTML5Boilerplate.

The database models include a count of term frequency per document, which
increases the running time of the loadarticles management command quite a bit.
The supplied list of 82 articles takes about 2 wall-clock minutes to ingest on
my system, and I expect larger files to take proportionally longer. The models
also include a means of retaining author order per document, so that the
article detail view presents the author list in the proper order.

In addition to the above minimum requirements, I added ranking of search results
by search term TF-IDF score, and an article detail view and a list of all
articles, available at '/articles/'. The search page itself will display
articles that match your search terms as you type, however the TF-IDF-ranking
of articles and the graph of authors' average TF-IDF for the terms will
not display until the form has been submitted, either by pressing the ENTER
key or by clicking the Submit button.

I also implemented a list of stop words, which reduce the number of terms
stored per article, thereby improving TF-IDF accuracy. The stop words are in
words.txt, as well as in the pubmed_search.utils module.


Installation
============
The application is intended for installation into a virtualenv with no site
packages, so begin installation by creating a new virtualenv. Once inside the
environment, use pip to install the requirements:

```
pip install -r requirements.txt
```

Next, create the database and collect static media:

```
python manage.py syncdb
python manage.py collectstatic
```

Load the JSON articles file via the import tool I wrote for the
purpose:

```
python manage.py loadarticles <filename>
```

Finally, run the test suite for the app:

```
python manage.py test pubmed_search
```


Running
=======
The application was written using Python 2.6, and should work without issue on
Python 2.7. It will likely also work on 2.5, though that has not been tested,
and will not work on 2.4 or earlier.

To run the development server, run:

```
python manage.py runserver
```

The application is set to use SQLite as its database; deploying the app to a
production setup is straight-forward, depending on anticipated load, but beyond
the scope of these instructions.

Tested Browsers
===============
I have tested the application on Firefox, Chrome and Safari. While the various
JavaScript libraries and the HTML5Boilerplate CSS modules all claim
compatibility with Internet Explorer 6+, I have not tested it with any version
of IE. While I expect the functionality to work, though more slowly than on a
modern browser, I expect the appearance to be somewhat degraded on earlier
versions of IE.
