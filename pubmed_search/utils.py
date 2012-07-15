## {{{ http://code.activestate.com/recipes/576611/ (r11)
# Author: Raymond Hettinger
# License: MIT
# Included to provide the Counter collection for Python 2.5-2.6
# Not needed if running on Python 2.7, as is included in stdlib
# as collections.Counter

from operator import itemgetter
from heapq import nlargest
from itertools import repeat, ifilter


class Counter(dict):
    '''Dict subclass for counting hashable objects.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> Counter('zyzygy')
    Counter({'y': 3, 'z': 2, 'g': 1})

    '''

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.
    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        '''Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    dict.update(self, iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)

    def copy(self):
        'Like dict.copy() but returns a Counter instance instead of a dict.'
        return Counter(self)

    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += Counter()
    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})


        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result


if __name__ == '__main__':
    import doctest
    print doctest.testmod()
## end of http://code.activestate.com/recipes/576611/ }}}

STOP_WORDS = ('a',
              'able',
              'about',
              'above',
              'abst',
              'accordance',
              'according',
              'accordingly',
              'across',
              'act',
              'actually',
              'added',
              'adj',
              'adopted',
              'affected',
              'affecting',
              'affects',
              'after',
              'afterwards',
              'again',
              'against',
              'ah',
              'all',
              'almost',
              'alone',
              'along',
              'already',
              'also',
              'although',
              'always',
              'am',
              'among',
              'amongst',
              'an',
              'and',
              'announce',
              'another',
              'any',
              'anybody',
              'anyhow',
              'anymore',
              'anyone',
              'anything',
              'anyway',
              'anyways',
              'anywhere',
              'apparently',
              'approximately',
              'are',
              'aren',
              'arent',
              'arise',
              'around',
              'as',
              'aside',
              'ask',
              'asking',
              'at',
              'auth',
              'available',
              'away',
              'awfully',
              'b',
              'back',
              'be',
              'became',
              'because',
              'become',
              'becomes',
              'becoming',
              'been',
              'before',
              'beforehand',
              'begin',
              'beginning',
              'beginnings',
              'begins',
              'behind',
              'being',
              'believe',
              'below',
              'beside',
              'besides',
              'between',
              'beyond',
              'biol',
              'both',
              'brief',
              'briefly',
              'but',
              'by',
              'c',
              'ca',
              'came',
              'can',
              'cannot',
              'cant',
              'cause',
              'causes',
              'certain',
              'certainly',
              'co',
              'com',
              'come',
              'comes',
              'contain',
              'containing',
              'contains',
              'could',
              'couldnt',
              'd',
              'date',
              'did',
              'didnt',
              'different',
              'do',
              'does',
              'doesnt',
              'doing',
              'done',
              'dont',
              'down',
              'downwards',
              'due',
              'during',
              'e',
              'each',
              'ed',
              'edu',
              'effect',
              'eg',
              'eight',
              'eighty',
              'either',
              'else',
              'elsewhere',
              'end',
              'ending',
              'enough',
              'especially',
              'et',
              'et-al',
              'etc',
              'even',
              'ever',
              'every',
              'everybody',
              'everyone',
              'everything',
              'everywhere',
              'ex',
              'except',
              'f',
              'far',
              'few',
              'ff',
              'fifth',
              'first',
              'five',
              'fix',
              'followed',
              'following',
              'follows',
              'for',
              'former',
              'formerly',
              'forth',
              'found',
              'four',
              'from',
              'further',
              'furthermore',
              'g',
              'gave',
              'get',
              'gets',
              'getting',
              'give',
              'given',
              'gives',
              'giving',
              'go',
              'goes',
              'gone',
              'got',
              'gotten',
              'h',
              'had',
              'happens',
              'hardly',
              'has',
              'hasnt',
              'have',
              'havent',
              'having',
              'he',
              'hed',
              'hence',
              'her',
              'here',
              'hereafter',
              'hereby',
              'herein',
              'heres',
              'hereupon',
              'hers',
              'herself',
              'hes',
              'hi',
              'hid',
              'him',
              'himself',
              'his',
              'hither',
              'home',
              'how',
              'howbeit',
              'however',
              'hundred',
              'i',
              'id',
              'ie',
              'if',
              'ill',
              'im',
              'immediate',
              'immediately',
              'importance',
              'important',
              'in',
              'inc',
              'indeed',
              'index',
              'information',
              'instead',
              'into',
              'invention',
              'inward',
              'is',
              'isnt',
              'it',
              'itd',
              'itll',
              'its',
              'itself',
              'ive',
              'j',
              'just',
              'k',
              'keep',
              'keeps',
              'kept',
              'keys',
              'kg',
              'km',
              'know',
              'known',
              'knows',
              'l',
              'largely',
              'last',
              'lately',
              'later',
              'latter',
              'latterly',
              'least',
              'less',
              'lest',
              'let',
              'lets',
              'like',
              'liked',
              'likely',
              'line',
              'little',
              'll',
              'look',
              'looking',
              'looks',
              'ltd',
              'm',
              'made',
              'mainly',
              'make',
              'makes',
              'many',
              'may',
              'maybe',
              'me',
              'mean',
              'means',
              'meantime',
              'meanwhile',
              'merely',
              'mg',
              'might',
              'million',
              'miss',
              'ml',
              'more',
              'moreover',
              'most',
              'mostly',
              'mr',
              'mrs',
              'much',
              'mug',
              'must',
              'my',
              'myself',
              'n',
              'na',
              'name',
              'namely',
              'nay',
              'nd',
              'near',
              'nearly',
              'necessarily',
              'necessary',
              'need',
              'needs',
              'neither',
              'never',
              'nevertheless',
              'new',
              'next',
              'nine',
              'ninety',
              'no',
              'nobody',
              'non',
              'none',
              'nonetheless',
              'noone',
              'nor',
              'normally',
              'nos',
              'not',
              'noted',
              'nothing',
              'now',
              'nowhere',
              'o',
              'obtain',
              'obtained',
              'obviously',
              'of',
              'off',
              'often',
              'oh',
              'ok',
              'okay',
              'old',
              'omitted',
              'on',
              'once',
              'one',
              'ones',
              'only',
              'onto',
              'or',
              'ord',
              'other',
              'others',
              'otherwise',
              'ought',
              'our',
              'ours',
              'ourselves',
              'out',
              'outside',
              'over',
              'overall',
              'owing',
              'own',
              'p',
              'page',
              'pages',
              'part',
              'particular',
              'particularly',
              'past',
              'per',
              'perhaps',
              'placed',
              'please',
              'plus',
              'poorly',
              'possible',
              'possibly',
              'potentially',
              'pp',
              'predominantly',
              'present',
              'previously',
              'primarily',
              'probably',
              'promptly',
              'proud',
              'provides',
              'put',
              'q',
              'que',
              'quickly',
              'quite',
              'qv',
              'r',
              'ran',
              'rather',
              'rd',
              're',
              'readily',
              'really',
              'recent',
              'recently',
              'ref',
              'refs',
              'regarding',
              'regardless',
              'regards',
              'related',
              'relatively',
              'research',
              'respectively',
              'resulted',
              'resulting',
              'results',
              'right',
              'run',
              's',
              'said',
              'same',
              'saw',
              'say',
              'saying',
              'says',
              'sec',
              'section',
              'see',
              'seeing',
              'seem',
              'seemed',
              'seeming',
              'seems',
              'seen',
              'self',
              'selves',
              'sent',
              'seven',
              'several',
              'shall',
              'she',
              'shed',
              'shell',
              'shes',
              'should',
              'shouldnt',
              'show',
              'showed',
              'shown',
              'showns',
              'shows',
              'significant',
              'significantly',
              'similar',
              'similarly',
              'since',
              'six',
              'slightly',
              'so',
              'some',
              'somebody',
              'somehow',
              'someone',
              'somethan',
              'something',
              'sometime',
              'sometimes',
              'somewhat',
              'somewhere',
              'soon',
              'sorry',
              'specifically',
              'specified',
              'specify',
              'specifying',
              'state',
              'states',
              'still',
              'stop',
              'strongly',
              'sub',
              'substantially',
              'successfully',
              'such',
              'sufficiently',
              'suggest',
              'sup',
              'sure',
              't',
              'take',
              'taken',
              'taking',
              'tell',
              'tends',
              'th',
              'than',
              'thank',
              'thanks',
              'thanx',
              'that',
              'thatll',
              'thats',
              'thatve',
              'the',
              'their',
              'theirs',
              'them',
              'themselves',
              'then',
              'thence',
              'there',
              'thereafter',
              'thereby',
              'thered',
              'therefore',
              'therein',
              'therell',
              'thereof',
              'therere',
              'theres',
              'thereto',
              'thereupon',
              'thereve',
              'these',
              'they',
              'theyd',
              'theyll',
              'theyre',
              'theyve',
              'think',
              'this',
              'those',
              'thou',
              'though',
              'thoughh',
              'thousand',
              'throug',
              'through',
              'throughout',
              'thru',
              'thus',
              'til',
              'tip',
              'to',
              'together',
              'too',
              'took',
              'toward',
              'towards',
              'tried',
              'tries',
              'truly',
              'try',
              'trying',
              'ts',
              'twice',
              'two',
              'u',
              'un',
              'under',
              'unfortunately',
              'unless',
              'unlike',
              'unlikely',
              'until',
              'unto',
              'up',
              'upon',
              'ups',
              'us',
              'use',
              'used',
              'useful',
              'usefully',
              'usefulness',
              'uses',
              'using',
              'usually',
              'v',
              'value',
              'various',
              've',
              'very',
              'via',
              'viz',
              'vol',
              'vols',
              'vs',
              'w',
              'want',
              'wants',
              'was',
              'wasnt',
              'way',
              'we',
              'wed',
              'welcome',
              'well',
              'went',
              'were',
              'werent',
              'weve',
              'what',
              'whatever',
              'whatll',
              'whats',
              'when',
              'whence',
              'whenever',
              'where',
              'whereafter',
              'whereas',
              'whereby',
              'wherein',
              'wheres',
              'whereupon',
              'wherever',
              'whether',
              'which',
              'while',
              'whim',
              'whither',
              'who',
              'whod',
              'whoever',
              'whole',
              'wholl',
              'whom',
              'whomever',
              'whos',
              'whose',
              'why',
              'widely',
              'willing',
              'wish',
              'with',
              'within',
              'without',
              'wont',
              'words',
              'world',
              'would',
              'wouldnt',
              'www',
              'x',
              'y',
              'yes',
              'yet',
              'you',
              'youd',
              'youll',
              'your',
              'youre',
              'yours',
              'yourself',
              'yourselves',
              'youve',
              'z',
              'zero')

import os.path
try:
    from collections import Counter
except ImportError:
    from pubmed_search.utils import Counter

from django.conf import settings
from django.utils import simplejson as json

from pubmed_search.models import Article, Author, Journal, Term, Frequency, Order
from pubmed_search.nlp import clean_term


def create_db_entries(record):
    """Given a JSON article, create DB model objects."""
    journal, journal_created = Journal.objects.get_or_create(name=record['journal'])

    article, article_created = Article.objects.get_or_create(pubmed_url=record['pubmedUrl'],
                                                             title=record['title'],
                                                             abstract=record['abstract'],
                                                             journal=journal)

    author_order = 0
    for item in record['authors']:
        lname, initials = item.split()
        author, author_created = Author.objects.get_or_create(initials=initials,
                                                              last_name=lname)
        order, order_created = Order.objects.get_or_create(author=author,
                                                           article=article,
                                                           order=author_order)
        author_order += 1

    raw_terms = ' '.join((record['title'],
                          record['abstract']))
    clean_terms = [clean_term(term) for term in raw_terms.split()]
    if settings.USE_STOP_WORDS:
        clean_terms = [term for term in clean_terms if term not in STOP_WORDS]
    cnt = Counter(clean_terms)
    for key, frequency in cnt.iteritems():
        term, term_created = Term.objects.get_or_create(term=key)
        freq, freq_created = Frequency.objects.get_or_create(term=term,
                                                             article=article,
                                                             frequency=frequency)


def load_json_from_file(filename):
    """Given a JSON file path, parses the file and loads the articles into the
    database."""
    file_path = os.path.normpath(filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path) as json_file:
            records = json.loads(json_file.read())
            for record in records:
                create_db_entries(record)

