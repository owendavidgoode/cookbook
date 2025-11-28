#!/usr/bin/env python3
"""
Generate ~3000 calendar facts from johndcook.com blog posts.
Output file: data/johndcook_calendar_candidates_v3.csv
"""

import json
import csv
import re
import html
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
import random

DATA_DIR = Path(__file__).parent.parent / "data"
POSTS_FILE = DATA_DIR / "johndcook_posts_enriched.jsonl"
OUTPUT_FILE = DATA_DIR / "johndcook_calendar_candidates_v3.csv"


def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_posts():
    """Load all posts from JSONL file."""
    posts = []
    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            post = json.loads(line)
            # Parse date
            post['date_obj'] = datetime.fromisoformat(post['date'].replace('Z', '+00:00').split('+')[0])
            post['year'] = post['date_obj'].year
            post['month'] = post['date_obj'].month
            post['day'] = post['date_obj'].day
            post['doy'] = post['date_obj'].timetuple().tm_yday
            post['weekday'] = post['date_obj'].strftime('%A')
            # Clean content
            post['plain_content'] = strip_html(post.get('content', ''))
            post['plain_title'] = strip_html(post.get('title', ''))
            posts.append(post)
    return posts


def count_links(content):
    """Count href links in HTML content."""
    return len(re.findall(r'href=', content, re.IGNORECASE))


def count_images(content):
    """Count img tags in HTML content."""
    return len(re.findall(r'<img\s', content, re.IGNORECASE))


def count_code_blocks(content):
    """Count pre/code blocks."""
    return len(re.findall(r'<pre[^>]*>', content, re.IGNORECASE))


def longest_code_block(content):
    """Find longest code block length."""
    blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', content, re.IGNORECASE | re.DOTALL)
    if not blocks:
        return 0
    return max(len(strip_html(b)) for b in blocks)


def has_math_symbol(text, symbol):
    """Check if text contains a math symbol."""
    return symbol in text


def term_appears(text, term, case_insensitive=True):
    """Check if a term appears in text."""
    if case_insensitive:
        return term.lower() in text.lower()
    return term in text


def count_sentences(text):
    """Roughly count sentences."""
    return len(re.findall(r'[.!?]+', text))


def count_paragraphs(content):
    """Count paragraph tags."""
    return len(re.findall(r'<p[^>]*>', content, re.IGNORECASE))


def extract_numbers(text):
    """Extract all numbers from text."""
    return re.findall(r'\b\d+(?:\.\d+)?\b', text)


def has_equation(content):
    """Check if post has LaTeX-style equations."""
    return bool(re.search(r'\$.*?\$|\\begin\{|\\frac|\\sum|\\int', content))


def generate_facts(posts):
    """Generate all candidate facts."""
    facts = []
    fact_id = 0

    def add_fact(fact_type, fact_text, link, date=None, slug=None):
        nonlocal fact_id
        fact_id += 1
        facts.append({
            'id': fact_id,
            'type': fact_type,
            'fact': fact_text,
            'source_link': link,
            'date': date or '',
            'slug': slug or ''
        })

    # Sort posts by date
    posts_sorted = sorted(posts, key=lambda p: p['date_obj'])

    # Build indices
    term_index = defaultdict(list)  # term -> [(post, count)]
    math_symbol_index = defaultdict(list)  # symbol -> [post]
    word_index = defaultdict(list)  # word -> [post]

    # Expanded notable terms to track
    notable_terms = [
        'Bayesian', 'Bayes', 'Markov', 'Fibonacci', 'golden ratio', 'prime',
        'Riemann', 'zeta', 'PDE', 'FFT', 'Monte Carlo', 'lambda', 'topology',
        'linear algebra', 'crypto', 'HIPAA', 'GDPR', 'CCPA', 'privacy',
        'machine learning', 'neural network', 'regex', 'Unicode', 'music',
        'elliptic curve', 'Fourier', 'Laplace', 'Bessel', 'gamma function',
        'beta function', 'factorial', 'binomial', 'Poisson', 'Gaussian',
        'normal distribution', 'chi-squared', 'exponential', 'logarithm',
        'trigonometry', 'calculus', 'differential equation', 'integral',
        'derivative', 'Taylor series', 'Maclaurin', 'continued fraction',
        'quaternion', 'complex analysis', 'number theory', 'graph theory',
        'combinatorics', 'probability', 'statistics', 'optimization',
        'Python', 'R language', 'Mathematica', 'MATLAB', 'Fortran', 'C++',
        'LaTeX', 'TeX', 'SQL', 'Unix', 'Linux', 'Windows', 'PowerShell',
        'cryptography', 'encryption', 'hash', 'Bitcoin', 'Monero',
        'Diffie-Hellman', 'RSA', 'AES', 'SHA', 'MD5', 'ECDSA',
        'Hamming', 'Shannon', 'information theory', 'entropy',
        'clinical trial', 'FDA', 'biostatistics', 'survival analysis',
        'consulting', 'freelance', 'interview', 'podcast',
        'Euler', 'Gauss', 'Ramanujan', 'Erdős', 'Knuth', 'Feynman',
        'pickle', 'pancake', 'pizza', 'coffee', 'tea', 'beer', 'wine',
        'cat', 'dog', 'elephant', 'dinosaur', 'Shakespeare', 'Bach', 'Mozart',
        # Additional terms for more facts
        'paradox', 'infinity', 'convergence', 'divergence', 'series',
        'sequence', 'limit', 'continuous', 'discontinuous', 'smooth',
        'analytic', 'holomorphic', 'meromorphic', 'singularity', 'pole',
        'residue', 'contour', 'integral', 'measure', 'Lebesgue',
        'Hilbert space', 'Banach space', 'metric space', 'topology',
        'manifold', 'differential', 'gradient', 'Hessian', 'Jacobian',
        'eigenvalue', 'eigenvector', 'matrix', 'determinant', 'trace',
        'rank', 'kernel', 'null space', 'column space', 'row space',
        'orthogonal', 'unitary', 'symmetric', 'Hermitian', 'positive definite',
        'SVD', 'QR', 'LU', 'Cholesky', 'Jordan form', 'diagonal',
        'sparse', 'dense', 'iterative', 'direct', 'numerical',
        'floating point', 'precision', 'accuracy', 'error', 'stability',
        'condition number', 'ill-conditioned', 'well-conditioned',
        'Newton', 'bisection', 'secant', 'fixed point', 'root finding',
        'interpolation', 'extrapolation', 'spline', 'polynomial',
        'Chebyshev', 'Legendre', 'Hermite', 'Laguerre', 'orthogonal polynomial',
        'quadrature', 'Simpson', 'trapezoidal', 'Gaussian quadrature',
        'ODE', 'IVP', 'BVP', 'Euler method', 'Runge-Kutta', 'Adams',
        'stiff', 'implicit', 'explicit', 'stability region',
        'finite difference', 'finite element', 'finite volume',
        'spectral method', 'collocation', 'Galerkin', 'variational',
        'wave equation', 'heat equation', 'Laplace equation', 'Poisson',
        'Navier-Stokes', 'fluid', 'turbulence', 'Reynolds number',
        'chaos', 'Lorenz', 'attractor', 'bifurcation', 'fractal',
        'Mandelbrot', 'Julia set', 'self-similar', 'dimension',
        'random walk', 'Brownian motion', 'diffusion', 'drift',
        'martingale', 'stopping time', 'optional stopping',
        'central limit theorem', 'law of large numbers', 'CLT', 'LLN',
        'confidence interval', 'hypothesis test', 'p-value', 'significance',
        'power', 'sample size', 'effect size', 'bootstrap', 'permutation',
        'regression', 'correlation', 'causation', 'confounding',
        'ANOVA', 'chi-square', 't-test', 'F-test', 'nonparametric',
        'Wilcoxon', 'Mann-Whitney', 'Kruskal-Wallis', 'Spearman', 'Kendall',
        'maximum likelihood', 'MLE', 'Bayesian inference', 'posterior',
        'prior', 'likelihood', 'conjugate', 'MCMC', 'Gibbs', 'Metropolis',
        'EM algorithm', 'expectation', 'maximization', 'latent',
        'mixture model', 'clustering', 'k-means', 'hierarchical',
        'PCA', 'factor analysis', 'ICA', 'dimension reduction',
        'classification', 'regression', 'decision tree', 'random forest',
        'boosting', 'bagging', 'ensemble', 'cross-validation', 'overfitting',
        'regularization', 'LASSO', 'ridge', 'elastic net', 'sparse',
        'SVM', 'support vector', 'kernel', 'RBF', 'polynomial kernel',
        'deep learning', 'CNN', 'RNN', 'LSTM', 'transformer', 'attention',
        'backpropagation', 'gradient descent', 'SGD', 'Adam', 'momentum',
        'batch normalization', 'dropout', 'activation', 'ReLU', 'sigmoid',
        'softmax', 'cross-entropy', 'loss function', 'objective',
        'hyperparameter', 'tuning', 'grid search', 'random search',
        'NLP', 'text', 'language model', 'embedding', 'word2vec',
        'sentiment', 'classification', 'NER', 'parsing', 'tokenization',
        'image', 'computer vision', 'object detection', 'segmentation',
        'speech', 'audio', 'signal processing', 'filter', 'convolution',
        'time series', 'forecasting', 'ARIMA', 'exponential smoothing',
        'seasonality', 'trend', 'stationarity', 'autocorrelation',
        'spectrum', 'periodogram', 'wavelet', 'Haar', 'Daubechies',
        'compression', 'encoding', 'decoding', 'lossy', 'lossless',
        'Huffman', 'arithmetic coding', 'LZW', 'JPEG', 'PNG', 'MP3',
        'error correction', 'Reed-Solomon', 'turbo code', 'LDPC',
        'modulation', 'demodulation', 'AM', 'FM', 'QAM', 'OFDM',
        'antenna', 'propagation', 'channel', 'fading', 'MIMO',
        'network', 'graph', 'node', 'edge', 'degree', 'path',
        'cycle', 'tree', 'forest', 'connected', 'component',
        'bipartite', 'planar', 'coloring', 'chromatic number',
        'clique', 'independent set', 'matching', 'cover',
        'flow', 'max flow', 'min cut', 'Ford-Fulkerson', 'Edmonds-Karp',
        'shortest path', 'Dijkstra', 'Bellman-Ford', 'Floyd-Warshall',
        'minimum spanning tree', 'Prim', 'Kruskal', 'Boruvka',
        'NP', 'NP-complete', 'NP-hard', 'P', 'polynomial time',
        'exponential time', 'complexity', 'big O', 'asymptotic',
        'algorithm', 'data structure', 'array', 'list', 'stack', 'queue',
        'heap', 'priority queue', 'hash table', 'binary search tree',
        'red-black tree', 'AVL tree', 'B-tree', 'trie', 'suffix tree',
        'sorting', 'quicksort', 'mergesort', 'heapsort', 'radix sort',
        'searching', 'binary search', 'linear search', 'interpolation search',
        'dynamic programming', 'memoization', 'greedy', 'divide and conquer',
        'recursion', 'iteration', 'tail recursion', 'stack overflow',
        'API', 'REST', 'HTTP', 'TCP', 'UDP', 'IP', 'DNS', 'SSL', 'TLS',
        'database', 'relational', 'NoSQL', 'MongoDB', 'PostgreSQL', 'MySQL',
        'cloud', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'microservice',
        'version control', 'Git', 'GitHub', 'GitLab', 'Bitbucket',
        'testing', 'unit test', 'integration test', 'TDD', 'BDD',
        'debugging', 'profiling', 'optimization', 'performance',
        'memory', 'cache', 'CPU', 'GPU', 'parallel', 'concurrent',
        'thread', 'process', 'lock', 'mutex', 'semaphore', 'deadlock',
        'distributed', 'consensus', 'Paxos', 'Raft', 'Byzantine',
        'blockchain', 'Ethereum', 'smart contract', 'DeFi', 'NFT',
        'quantum', 'qubit', 'superposition', 'entanglement', 'Shor',
        'Grover', 'quantum computing', 'quantum cryptography',
    ]

    math_symbols = ['π', 'φ', 'Φ', 'τ', 'ζ', '∞', '∫', '∑', '∏', '√', 'Γ', 'Δ', 'Ω', 'α', 'β', 'γ', 'δ', 'ε', 'θ', 'λ', 'μ', 'σ', 'ω', 'ρ', 'ξ', 'η', 'ψ', 'χ', 'ν', 'κ', 'ι']

    # More search terms for rare word hunting
    rare_word_candidates = [
        'abracadabra', 'zigzag', 'palindrome', 'anagram', 'acronym',
        'oxymoron', 'onomatopoeia', 'synecdoche', 'metonymy', 'hyperbole',
        'chiasmus', 'zeugma', 'tmesis', 'litotes', 'meiosis',
        'sesquipedalian', 'defenestration', 'floccinaucinihilipilification',
        'antidisestablishmentarianism', 'supercalifragilisticexpialidocious',
        'pneumonoultramicroscopicsilicovolcanoconiosis',
        'hippopotomonstrosesquippedaliophobia', 'honorificabilitudinity',
        'quizzaciously', 'oxyphenbutazone', 'uncopyrightable',
        'dermatoglyphics', 'misconjugatedly', 'ambidextrously',
        'facetiously', 'abstemiously', 'arsenious', 'caesious',
        'syzygy', 'cwm', 'crwth', 'cwtch', 'tsktsks',
        'rhythms', 'glycyrrhizin', 'twyndyllyngs', 'strengths',
        'euouae', 'psych', 'glyph', 'lymph', 'nymph', 'pygmy',
        'tryst', 'myrrh', 'crypt', 'gypsy', 'lynch', 'synth',
        'flyby', 'dryly', 'slyly', 'wryly', 'shyly', 'spryly',
        'xylyl', 'phpht', 'tsksk', 'crwth', 'cwtch', 'grrl',
        'pfft', 'psst', 'shh', 'hmm', 'brr', 'grr', 'zzz',
        'aardvark', 'aardwolf', 'abacus', 'abalone', 'abandon',
        'zephyr', 'zeppelin', 'zero', 'zest', 'zigzag', 'zinc',
        'zodiac', 'zombie', 'zone', 'zoo', 'zoom', 'zucchini',
        'quasar', 'quark', 'quantum', 'quarantine', 'quartz',
        'xylophone', 'xenon', 'xerox', 'x-ray', 'xylem',
    ]

    # Process each post
    for post in posts:
        content = post['plain_content']
        title = post['plain_title']
        full_text = title + ' ' + content

        # Track term occurrences
        for term in notable_terms:
            count = len(re.findall(r'\b' + re.escape(term) + r'\b', full_text, re.IGNORECASE))
            if count > 0:
                term_index[term.lower()].append((post, count))

        # Track math symbols
        for sym in math_symbols:
            if sym in full_text:
                math_symbol_index[sym].append(post)

        # Track rare words
        for word in rare_word_candidates:
            if re.search(r'\b' + re.escape(word) + r'\b', full_text, re.IGNORECASE):
                word_index[word.lower()].append(post)

    # === RARITY FACTS ===
    # Terms that appear only once or very few times
    for term in notable_terms:
        occurrences = term_index.get(term.lower(), [])
        if len(occurrences) == 1:
            post, _ = occurrences[0]
            add_fact(
                'rarity',
                f"The word '{term}' appears in only one blog post: \"{post['plain_title']}\" on {post['date_obj'].strftime('%B %d, %Y')}.",
                post['link'],
                post['date'],
                post['slug']
            )
        elif 2 <= len(occurrences) <= 3:
            post_titles = [f"\"{p['plain_title']}\" ({p['date_obj'].strftime('%Y')})" for p, _ in occurrences[:3]]
            add_fact(
                'rarity',
                f"The term '{term}' appears in only {len(occurrences)} posts across the entire blog: {', '.join(post_titles)}.",
                occurrences[0][0]['link'],
                occurrences[0][0]['date'],
                occurrences[0][0]['slug']
            )
        elif 4 <= len(occurrences) <= 10:
            add_fact(
                'rarity',
                f"The term '{term}' appears in exactly {len(occurrences)} posts, spanning from {min(occurrences, key=lambda x: x[0]['date_obj'])[0]['year']} to {max(occurrences, key=lambda x: x[0]['date_obj'])[0]['year']}.",
                occurrences[0][0]['link']
            )

    # Rare word facts
    for word, word_posts in word_index.items():
        if len(word_posts) == 1:
            post = word_posts[0]
            add_fact(
                'rarity',
                f"The unusual word '{word}' appears in only one post: \"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}).",
                post['link'],
                post['date'],
                post['slug']
            )

    # === FIRST/LAST OCCURRENCE FACTS ===
    first_last_terms = list(set([
        'Bayesian', 'machine learning', 'Python', 'crypto', 'Bitcoin', 'Monero',
        'HIPAA', 'GDPR', 'Fibonacci', 'Riemann', 'elliptic curve', 'neural network',
        'PowerShell', 'Unicode', 'Diffie-Hellman', 'RSA', 'blockchain', 'quantum',
        'deep learning', 'transformer', 'attention', 'GPT', 'LLM', 'ChatGPT',
        'Docker', 'Kubernetes', 'cloud', 'AWS', 'microservice', 'API',
        'COVID', 'pandemic', 'vaccine', 'clinical trial', 'FDA',
        'privacy', 'CCPA', 'anonymization', 'de-identification',
        'Fourier', 'Laplace', 'Bessel', 'gamma function', 'zeta function',
        'Monte Carlo', 'bootstrap', 'MCMC', 'Gibbs sampling',
        'SVD', 'PCA', 'eigenvalue', 'matrix', 'tensor',
        'regex', 'LaTeX', 'Markdown', 'HTML', 'CSS', 'JavaScript',
        'consulting', 'freelance', 'entrepreneur', 'startup',
    ]))

    for term in first_last_terms:
        occurrences = term_index.get(term.lower(), [])
        if occurrences:
            # First occurrence
            first_post = min(occurrences, key=lambda x: x[0]['date_obj'])[0]
            add_fact(
                'first',
                f"The first mention of '{term}' on the blog was on {first_post['date_obj'].strftime('%B %d, %Y')} in \"{first_post['plain_title']}\".",
                first_post['link'],
                first_post['date'],
                first_post['slug']
            )
            # Last occurrence (if different and blog has been around)
            last_post = max(occurrences, key=lambda x: x[0]['date_obj'])[0]
            if last_post['id'] != first_post['id'] and len(occurrences) > 3:
                add_fact(
                    'last',
                    f"The most recent post mentioning '{term}' is \"{last_post['plain_title']}\" from {last_post['date_obj'].strftime('%B %d, %Y')}.",
                    last_post['link'],
                    last_post['date'],
                    last_post['slug']
                )

    # === MATH SYMBOL FACTS ===
    for sym, sym_posts in math_symbol_index.items():
        if len(sym_posts) == 1:
            post = sym_posts[0]
            add_fact(
                'constant',
                f"The symbol {sym} appears in only one post: \"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}).",
                post['link'],
                post['date'],
                post['slug']
            )
        elif 2 <= len(sym_posts) <= 5:
            add_fact(
                'constant',
                f"The Greek letter {sym} appears in exactly {len(sym_posts)} posts on the blog.",
                sym_posts[0]['link']
            )
        elif len(sym_posts) >= 10:
            add_fact(
                'constant',
                f"The mathematical symbol {sym} appears across {len(sym_posts)} different posts on the blog.",
                sym_posts[0]['link']
            )

    # === OUTLIER FACTS ===
    # Longest posts
    posts_by_length = sorted(posts, key=lambda p: p.get('word_count', 0), reverse=True)
    for i, post in enumerate(posts_by_length[:20]):
        add_fact(
            'density',
            f"The #{i+1} longest post is \"{post['plain_title']}\" with {post.get('word_count', 0):,} words, published {post['date_obj'].strftime('%B %d, %Y')}.",
            post['link'],
            post['date'],
            post['slug']
        )

    # Shortest posts
    posts_with_content = [p for p in posts if p.get('word_count', 0) > 10]
    posts_by_length_asc = sorted(posts_with_content, key=lambda p: p.get('word_count', 0))
    for i, post in enumerate(posts_by_length_asc[:20]):
        add_fact(
            'density',
            f"One of the shortest posts is \"{post['plain_title']}\" with just {post.get('word_count', 0)} words ({post['date_obj'].strftime('%Y')}).",
            post['link'],
            post['date'],
            post['slug']
        )

    # Most links
    for post in posts:
        post['link_count'] = count_links(post.get('content', ''))
    posts_by_links = sorted(posts, key=lambda p: p['link_count'], reverse=True)
    for i, post in enumerate(posts_by_links[:20]):
        if post['link_count'] > 3:
            add_fact(
                'density',
                f"\"{post['plain_title']}\" contains {post['link_count']} links, making it one of the most link-rich posts on the blog.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Most images
    for post in posts:
        post['image_count'] = count_images(post.get('content', ''))
    posts_by_images = sorted(posts, key=lambda p: p['image_count'], reverse=True)
    for i, post in enumerate(posts_by_images[:20]):
        if post['image_count'] > 2:
            add_fact(
                'density',
                f"\"{post['plain_title']}\" includes {post['image_count']} images, one of the most visual posts on the blog.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Most code blocks
    for post in posts:
        post['code_count'] = count_code_blocks(post.get('content', ''))
    posts_by_code = sorted(posts, key=lambda p: p['code_count'], reverse=True)
    for i, post in enumerate(posts_by_code[:20]):
        if post['code_count'] > 1:
            add_fact(
                'density',
                f"\"{post['plain_title']}\" has {post['code_count']} code blocks, reflecting the blog's emphasis on practical programming.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Longest code block
    for post in posts:
        post['longest_code'] = longest_code_block(post.get('content', ''))
    posts_by_longest_code = sorted(posts, key=lambda p: p['longest_code'], reverse=True)
    for i, post in enumerate(posts_by_longest_code[:15]):
        if post['longest_code'] > 200:
            add_fact(
                'density',
                f"\"{post['plain_title']}\" contains a code block of {post['longest_code']} characters, one of the longest on the blog.",
                post['link'],
                post['date'],
                post['slug']
            )

    # === YEAR STATISTICS ===
    year_counts = Counter(p['year'] for p in posts)
    for year, count in year_counts.most_common():
        add_fact(
            'quirk',
            f"In {year}, {count} posts were published on the blog.",
            posts_sorted[-1]['link']
        )

    # Year-over-year changes
    years_sorted = sorted(year_counts.keys())
    for i in range(1, len(years_sorted)):
        prev_year = years_sorted[i-1]
        curr_year = years_sorted[i]
        prev_count = year_counts[prev_year]
        curr_count = year_counts[curr_year]
        if prev_count > 0:
            change = ((curr_count - prev_count) / prev_count) * 100
            if abs(change) > 20:
                direction = "increased" if change > 0 else "decreased"
                add_fact(
                    'quirk',
                    f"Blog output {direction} by {abs(change):.0f}% from {prev_year} ({prev_count} posts) to {curr_year} ({curr_count} posts).",
                    posts_sorted[-1]['link']
                )

    # === WEEKDAY STATISTICS ===
    weekday_counts = Counter(p['weekday'] for p in posts)
    for day, count in weekday_counts.most_common():
        add_fact(
            'quirk',
            f"{day} has {count} blog posts published on that day of the week.",
            posts_sorted[-1]['link']
        )

    # === MONTH STATISTICS ===
    month_counts = Counter(p['month'] for p in posts)
    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    for month, count in month_counts.most_common():
        add_fact(
            'quirk',
            f"{month_names[month]} has seen {count} blog posts over the years.",
            posts_sorted[-1]['link']
        )

    # === CATEGORY STATISTICS ===
    category_counts = Counter()
    for post in posts:
        for cat in post.get('category_names', []):
            category_counts[cat] += 1

    for cat, count in category_counts.most_common():
        if cat != 'Uncategorized':
            add_fact(
                'quirk',
                f"The '{cat}' category contains {count} posts.",
                posts_sorted[-1]['link']
            )

    # Category by year trends
    cat_year = defaultdict(lambda: Counter())
    for post in posts:
        for cat in post.get('category_names', []):
            cat_year[cat][post['year']] += 1

    for cat in ['Math', 'Computing', 'Statistics', 'Python', 'Music', 'Science']:
        if cat in cat_year:
            years_data = cat_year[cat]
            peak_year = max(years_data.items(), key=lambda x: x[1])
            add_fact(
                'quirk',
                f"The peak year for '{cat}' posts was {peak_year[0]} with {peak_year[1]} posts in that category.",
                posts_sorted[-1]['link']
            )

    # === ON THIS DAY FACTS - EXPANDED ===
    # Group posts by month-day
    doy_posts = defaultdict(list)
    for post in posts:
        key = (post['month'], post['day'])
        doy_posts[key].append(post)

    # For each day of year with posts, generate multiple facts
    for (month, day), day_posts in doy_posts.items():
        month_name = datetime(2000, month, day).strftime('%B')

        # Best post by word count
        if len(day_posts) >= 1:
            best_post = max(day_posts, key=lambda p: p.get('word_count', 0))
            add_fact(
                'otd',
                f"On {month_name} {day}, {best_post['year']}: \"{best_post['plain_title']}\" was published ({best_post.get('word_count', 0)} words).",
                best_post['link'],
                best_post['date'],
                best_post['slug']
            )

        # Oldest post on this day
        if len(day_posts) >= 2:
            oldest_post = min(day_posts, key=lambda p: p['date_obj'])
            add_fact(
                'otd',
                f"The earliest {month_name} {day} post was \"{oldest_post['plain_title']}\" in {oldest_post['year']}.",
                oldest_post['link'],
                oldest_post['date'],
                oldest_post['slug']
            )

        # Newest post on this day
        if len(day_posts) >= 2:
            newest_post = max(day_posts, key=lambda p: p['date_obj'])
            add_fact(
                'otd',
                f"The most recent {month_name} {day} post was \"{newest_post['plain_title']}\" in {newest_post['year']}.",
                newest_post['link'],
                newest_post['date'],
                newest_post['slug']
            )

        # If multiple posts on same day of year across years, note that
        if len(day_posts) >= 3:
            years = sorted(set(p['year'] for p in day_posts))
            add_fact(
                'otd',
                f"{month_name} {day} has seen {len(day_posts)} blog posts over the years ({years[0]}-{years[-1]}).",
                day_posts[0]['link']
            )

        # Random interesting post from this day
        if len(day_posts) >= 3:
            random.seed(month * 100 + day)  # Deterministic
            random_post = random.choice(day_posts)
            add_fact(
                'otd',
                f"A {month_name} {day} highlight: \"{random_post['plain_title']}\" ({random_post['year']}).",
                random_post['link'],
                random_post['date'],
                random_post['slug']
            )

    # === TITLE QUIRKS ===
    # Shortest titles
    posts_by_title_len = sorted(posts, key=lambda p: len(p['plain_title']))
    for post in posts_by_title_len[:20]:
        if len(post['plain_title']) <= 20:
            add_fact(
                'quirk',
                f"The post titled \"{post['plain_title']}\" has one of the shortest titles on the blog, at just {len(post['plain_title'])} characters.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Longest titles
    for post in posts_by_title_len[-20:]:
        if len(post['plain_title']) >= 50:
            add_fact(
                'quirk',
                f"At {len(post['plain_title'])} characters, \"{post['plain_title'][:40]}...\" is one of the longest post titles.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Question titles
    question_posts = [p for p in posts if '?' in p['plain_title']]
    add_fact(
        'quirk',
        f"{len(question_posts)} posts have titles containing a question mark, showing the blog's exploratory nature.",
        question_posts[0]['link'] if question_posts else posts[0]['link']
    )

    # Individual question title posts
    for post in question_posts[:50]:
        add_fact(
            'quirk',
            f"The question \"{post['plain_title']}\" was explored on {post['date_obj'].strftime('%B %d, %Y')}.",
            post['link'],
            post['date'],
            post['slug']
        )

    # Titles starting with "How"
    how_posts = [p for p in posts if p['plain_title'].lower().startswith('how')]
    for post in how_posts[:30]:
        add_fact(
            'quirk',
            f"\"{post['plain_title']}\" - a how-to from {post['date_obj'].strftime('%Y')}.",
            post['link'],
            post['date'],
            post['slug']
        )

    # Titles starting with "Why"
    why_posts = [p for p in posts if p['plain_title'].lower().startswith('why')]
    for post in why_posts[:30]:
        add_fact(
            'quirk',
            f"\"{post['plain_title']}\" - exploring the why, from {post['date_obj'].strftime('%Y')}.",
            post['link'],
            post['date'],
            post['slug']
        )

    # Titles with numbers
    number_title_posts = [p for p in posts if re.search(r'\d+', p['plain_title'])]
    for post in number_title_posts[:50]:
        add_fact(
            'quirk',
            f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) - one of {len(number_title_posts)} posts with numbers in the title.",
            post['link'],
            post['date'],
            post['slug']
        )

    # === SPECIAL CONTENT FACTS ===
    # Posts mentioning pi (π)
    pi_posts = [p for p in posts if 'π' in p['plain_content'] or '3.14159' in p['plain_content']]
    if pi_posts:
        add_fact(
            'constant',
            f"The mathematical constant π appears in {len(pi_posts)} posts across the blog.",
            pi_posts[0]['link']
        )
        for post in pi_posts[:20]:
            add_fact(
                'constant',
                f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) discusses the constant π.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Posts mentioning e (Euler's number)
    e_posts = [p for p in posts if "Euler's number" in p['plain_content'] or '2.71828' in p['plain_content'] or re.search(r'\be\s*[=≈]', p['plain_content'])]
    if e_posts:
        add_fact(
            'constant',
            f"Euler's number e is discussed in {len(e_posts)} posts.",
            e_posts[0]['link']
        )

    # Posts mentioning golden ratio
    golden_posts = term_index.get('golden ratio', [])
    if golden_posts:
        add_fact(
            'constant',
            f"The golden ratio (φ ≈ 1.618) appears in {len(golden_posts)} posts.",
            golden_posts[0][0]['link']
        )

    # === SPECIAL TOPIC COUNTS ===
    # Cryptography posts
    crypto_posts = [p for p in posts if any(term_appears(p['plain_content'], t) for t in ['cryptography', 'encryption', 'cipher', 'hash function', 'public key', 'private key'])]
    if crypto_posts:
        add_fact(
            'quirk',
            f"The blog contains {len(crypto_posts)} posts touching on cryptography, encryption, or ciphers.",
            crypto_posts[0]['link']
        )
        for post in crypto_posts[:30]:
            add_fact(
                'quirk',
                f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) covers cryptography topics.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Privacy posts
    privacy_posts = [p for p in posts if any(term_appears(p['plain_content'], t) for t in ['privacy', 'HIPAA', 'GDPR', 'anonymization', 'de-identification', 'PII', 'PHI'])]
    if privacy_posts:
        add_fact(
            'quirk',
            f"Data privacy topics (HIPAA, GDPR, anonymization) appear in {len(privacy_posts)} posts.",
            privacy_posts[0]['link']
        )
        for post in privacy_posts[:20]:
            add_fact(
                'quirk',
                f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) discusses data privacy.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Music posts
    music_posts = [p for p in posts if 'Music' in p.get('category_names', [])]
    if music_posts:
        add_fact(
            'quirk',
            f"The blog has {len(music_posts)} posts in the Music category, exploring the intersection of math and music.",
            music_posts[0]['link']
        )
        for post in music_posts[:30]:
            add_fact(
                'quirk',
                f"\"{post['plain_title']}\" - where math meets music ({post['date_obj'].strftime('%Y')}).",
                post['link'],
                post['date'],
                post['slug']
            )

    # Science posts
    science_posts = [p for p in posts if 'Science' in p.get('category_names', [])]
    for post in science_posts[:30]:
        add_fact(
            'quirk',
            f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) - a science-focused post.",
            post['link'],
            post['date'],
            post['slug']
        )

    # === INTERVIEW/PODCAST FACTS ===
    interview_posts = [p for p in posts if any(term_appears(p['plain_title'] + ' ' + p['plain_content'], t) for t in ['interview', 'podcast', 'Q&A', 'conversation with'])]
    if interview_posts:
        for post in interview_posts[:15]:
            add_fact(
                'quirk',
                f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) features interview or Q&A content.",
                post['link'],
                post['date'],
                post['slug']
            )

    # === QUOTE FACTS ===
    # Posts with blockquotes
    blockquote_posts = [p for p in posts if '<blockquote' in p.get('content', '')]
    if blockquote_posts:
        add_fact(
            'quirk',
            f"{len(blockquote_posts)} posts contain blockquotes, often featuring quotes from mathematicians and scientists.",
            blockquote_posts[0]['link']
        )
        for post in blockquote_posts[:30]:
            add_fact(
                'quirk',
                f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) includes notable quotations.",
                post['link'],
                post['date'],
                post['slug']
            )

    # === MATHEMATICIAN/SCIENTIST MENTIONS ===
    mathematicians = [
        'Euler', 'Gauss', 'Riemann', 'Ramanujan', 'Erdős', 'Knuth', 'Feynman',
        'Newton', 'Leibniz', 'Fermat', 'Cauchy', 'Laplace', 'Fourier', 'Hilbert',
        'Gödel', 'Turing', 'Shannon', 'von Neumann', 'Poincaré', 'Kolmogorov',
        'Bayes', 'Fisher', 'Pearson', 'Student', 'Gosset', 'Galton',
        'Bernoulli', 'Chebyshev', 'Markov', 'Poisson', 'Weierstrass',
        'Cantor', 'Dedekind', 'Peano', 'Russell', 'Whitehead', 'Frege',
        'Boole', 'de Morgan', 'Venn', 'Cayley', 'Hamilton', 'Sylvester',
        'Noether', 'Hardy', 'Littlewood', 'Wiener', 'Mandelbrot', 'Penrose',
        'Hawking', 'Einstein', 'Dirac', 'Schrödinger', 'Heisenberg', 'Bohr',
        'Maxwell', 'Boltzmann', 'Planck', 'Curie', 'Lorentz', 'Minkowski',
        'Archimedes', 'Pythagoras', 'Euclid', 'Apollonius', 'Diophantus',
        'al-Khwarizmi', 'Fibonacci', 'Cardano', 'Vieta', 'Descartes', 'Pascal',
        'Huygens', 'Hooke', 'Napier', 'Briggs', 'Wallis', 'Barrow',
        'L\'Hôpital', 'Taylor', 'Maclaurin', 'Stirling', 'Lagrange', 'Legendre',
        'Abel', 'Galois', 'Jacobi', 'Dirichlet', 'Kummer', 'Kronecker',
        'Klein', 'Lie', 'Cartan', 'Weyl', 'Weil', 'Grothendieck', 'Serre',
        'Atiyah', 'Singer', 'Milnor', 'Smale', 'Thurston', 'Perelman',
        'Wiles', 'Tao', 'Villani', 'Mirzakhani', 'Scholze',
    ]
    for mathematician in mathematicians:
        mentions = term_index.get(mathematician.lower(), [])
        if len(mentions) >= 5:
            add_fact(
                'quirk',
                f"{mathematician} is mentioned in {len(mentions)} posts on the blog.",
                mentions[0][0]['link']
            )
        elif len(mentions) == 1:
            post = mentions[0][0]
            add_fact(
                'rarity',
                f"{mathematician} is mentioned in only one post: \"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}).",
                post['link'],
                post['date'],
                post['slug']
            )
        elif 2 <= len(mentions) <= 4:
            add_fact(
                'rarity',
                f"{mathematician} appears in exactly {len(mentions)} posts on the blog.",
                mentions[0][0]['link']
            )

    # === PROGRAMMING LANGUAGE FACTS ===
    prog_languages = [
        'Python', 'R', 'Mathematica', 'MATLAB', 'Fortran', 'C++', 'C#',
        'Haskell', 'Lisp', 'Scheme', 'Clojure', 'Julia', 'Perl', 'Ruby',
        'JavaScript', 'TypeScript', 'PowerShell', 'Bash', 'Shell',
        'Java', 'Scala', 'Kotlin', 'Go', 'Rust', 'Swift', 'Objective-C',
        'PHP', 'SQL', 'Assembly', 'COBOL', 'Pascal', 'Ada', 'Prolog',
        'Erlang', 'Elixir', 'F#', 'OCaml', 'SML', 'Racket',
        'Lua', 'Tcl', 'AWK', 'Sed', 'Vim', 'Emacs',
    ]
    for lang in prog_languages:
        lang_posts = term_index.get(lang.lower(), [])
        if len(lang_posts) >= 10:
            add_fact(
                'quirk',
                f"{lang} code or discussion appears in {len(lang_posts)} posts.",
                lang_posts[0][0]['link']
            )
        elif 1 <= len(lang_posts) <= 5:
            for post, _ in lang_posts[:3]:
                add_fact(
                    'rarity',
                    f"{lang} is mentioned in \"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}).",
                    post['link'],
                    post['date'],
                    post['slug']
                )

    # === SPECIAL DATE FACTS ===
    special_dates = [
        ((3, 14), "Pi Day", "π ≈ 3.14"),
        ((2, 7), "e Day", "e ≈ 2.7"),
        ((6, 28), "Tau Day", "τ = 2π ≈ 6.28"),
        ((10, 23), "Mole Day", "Avogadro's number 6.02×10²³"),
        ((3, 4), "Grammar Day", "March forth!"),
        ((5, 4), "Star Wars Day", "May the Fourth"),
        ((9, 2), "Calendar Reform Day", "Sept 2, 1752"),
        ((4, 1), "April Fools' Day", "mathematical jokes"),
        ((11, 23), "Fibonacci Day", "1-1-2-3"),
        ((1, 1), "New Year's Day", "new beginnings"),
        ((7, 4), "Independence Day", "US holiday"),
        ((12, 25), "Christmas Day", "holiday"),
        ((10, 31), "Halloween", "spooky math"),
        ((2, 14), "Valentine's Day", "love and math"),
        ((3, 17), "St. Patrick's Day", "green"),
        ((7, 22), "Pi Approximation Day", "22/7 ≈ π"),
        ((2, 29), "Leap Day", "rare date"),
        ((11, 11), "Veterans Day", "11/11"),
        ((12, 31), "New Year's Eve", "end of year"),
    ]

    for (month, day), name, reason in special_dates:
        special_posts = [p for p in posts if p['month'] == month and p['day'] == day]
        if special_posts:
            add_fact(
                'otd',
                f"{name} ({month}/{day}, {reason}) has seen {len(special_posts)} blog posts.",
                special_posts[0]['link']
            )
            for post in special_posts[:5]:
                add_fact(
                    'otd',
                    f"On {name} {post['year']}: \"{post['plain_title']}\" was published.",
                    post['link'],
                    post['date'],
                    post['slug']
                )

    # === WORD/PHRASE HUNTING - EXPANDED ===
    quirky_terms = [
        'pickle', 'pancake', 'pizza', 'coffee', 'tea', 'beer', 'wine',
        'theorem', 'proof', 'conjecture', 'lemma', 'corollary', 'axiom',
        'paradox', 'puzzle', 'trick', 'magic', 'elegant', 'beautiful',
        'ugly', 'disaster', 'mistake', 'bug', 'error', 'glitch',
        'consulting', 'client', 'project', 'deadline', 'budget',
        'cat', 'dog', 'rabbit', 'turtle', 'frog', 'bird',
        'apple', 'orange', 'banana', 'strawberry', 'cherry',
        'red', 'blue', 'green', 'yellow', 'purple', 'orange',
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'spring', 'summer', 'autumn', 'winter', 'fall',
        'sunrise', 'sunset', 'midnight', 'noon', 'dawn', 'dusk',
        'mountain', 'river', 'ocean', 'forest', 'desert', 'island',
        'Texas', 'Houston', 'Austin', 'Dallas', 'San Antonio',
        'NASA', 'SpaceX', 'rocket', 'satellite', 'orbit', 'moon',
        'chess', 'poker', 'bridge', 'sudoku', 'crossword', 'wordle',
        'golf', 'tennis', 'baseball', 'basketball', 'football', 'soccer',
        'piano', 'guitar', 'violin', 'drum', 'trumpet', 'flute',
        'Bach', 'Mozart', 'Beethoven', 'Chopin', 'Liszt', 'Brahms',
        'Shakespeare', 'Dickens', 'Austen', 'Hemingway', 'Tolkien',
        'Homer', 'Dante', 'Cervantes', 'Dostoevsky', 'Tolstoy',
        'love', 'hate', 'fear', 'joy', 'anger', 'surprise',
        'happy', 'sad', 'angry', 'scared', 'excited', 'bored',
        'simple', 'complex', 'easy', 'hard', 'fast', 'slow',
        'big', 'small', 'tall', 'short', 'wide', 'narrow',
        'old', 'new', 'ancient', 'modern', 'future', 'past',
        'true', 'false', 'maybe', 'probably', 'certainly', 'unlikely',
        'always', 'never', 'sometimes', 'often', 'rarely', 'occasionally',
    ]

    for term in quirky_terms:
        occurrences = term_index.get(term.lower(), [])
        if len(occurrences) == 1:
            post = occurrences[0][0]
            add_fact(
                'rarity',
                f"Only one post mentions '{term}': \"{post['plain_title']}\" on {post['date_obj'].strftime('%B %d, %Y')}.",
                post['link'],
                post['date'],
                post['slug']
            )
        elif 2 <= len(occurrences) <= 5:
            add_fact(
                'rarity',
                f"The word '{term}' appears in only {len(occurrences)} posts across the entire blog.",
                occurrences[0][0]['link']
            )
        elif len(occurrences) > 20:
            add_fact(
                'quirk',
                f"The word '{term}' appears in {len(occurrences)} posts.",
                occurrences[0][0]['link']
            )

    # === CATEGORY COMBOS ===
    # Posts in multiple categories
    multi_cat_posts = [p for p in posts if len(p.get('category_names', [])) >= 2]
    for post in multi_cat_posts[:50]:
        cats = ', '.join(post.get('category_names', []))
        add_fact(
            'quirk',
            f"\"{post['plain_title']}\" spans {len(post.get('category_names', []))} categories: {cats}.",
            post['link'],
            post['date'],
            post['slug']
        )

    # === MILESTONE POSTS ===
    # Posts by ID (roughly chronological)
    sorted_by_id = sorted(posts, key=lambda p: p['id'])
    milestones = [1, 10, 50, 100, 200, 300, 400, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    for milestone in milestones:
        if milestone <= len(sorted_by_id):
            post = sorted_by_id[milestone - 1]
            add_fact(
                'quirk',
                f"The {milestone}th post on the blog was \"{post['plain_title']}\" on {post['date_obj'].strftime('%B %d, %Y')}.",
                post['link'],
                post['date'],
                post['slug']
            )

    # Total post count
    add_fact(
        'quirk',
        f"The blog contains {len(posts)} posts spanning from {posts_sorted[0]['year']} to {posts_sorted[-1]['year']}.",
        posts_sorted[-1]['link']
    )

    # === PUBLICATION FREQUENCY ===
    # Posts per month
    month_counts = Counter((p['year'], p['month']) for p in posts)

    # Top 20 months
    for (year, month), count in month_counts.most_common(20):
        add_fact(
            'quirk',
            f"{datetime(year, month, 1).strftime('%B %Y')} had {count} posts.",
            posts_sorted[-1]['link']
        )

    # === TAG STATISTICS ===
    tag_counts = Counter()
    for post in posts:
        for tag in post.get('tag_names', []):
            tag_counts[tag] += 1

    for tag, count in tag_counts.most_common(50):
        add_fact(
            'quirk',
            f"The tag '{tag}' has been used {count} times across the blog.",
            posts_sorted[-1]['link']
        )

    # Rare tags
    for tag, count in tag_counts.items():
        if count == 1:
            # Find the post with this tag
            for post in posts:
                if tag in post.get('tag_names', []):
                    add_fact(
                        'rarity',
                        f"The tag '{tag}' was used exactly once, in \"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}).",
                        post['link'],
                        post['date'],
                        post['slug']
                    )
                    break
        elif count == 2:
            posts_with_tag = [p for p in posts if tag in p.get('tag_names', [])]
            if len(posts_with_tag) >= 2:
                add_fact(
                    'rarity',
                    f"The tag '{tag}' was used exactly twice: \"{posts_with_tag[0]['plain_title']}\" and \"{posts_with_tag[1]['plain_title']}\".",
                    posts_with_tag[0]['link']
                )

    # === SERIES DETECTION ===
    # Posts with "Part" in title
    series_posts = [p for p in posts if re.search(r'\bPart\s+\d+\b', p['plain_title'], re.IGNORECASE) or re.search(r'\(\d+\s*of\s*\d+\)', p['plain_title'])]
    if series_posts:
        add_fact(
            'quirk',
            f"The blog contains {len(series_posts)} posts that are explicitly part of a series.",
            series_posts[0]['link']
        )
        for post in series_posts[:20]:
            add_fact(
                'quirk',
                f"\"{post['plain_title']}\" ({post['date_obj'].strftime('%Y')}) is part of a series.",
                post['link'],
                post['date'],
                post['slug']
            )

    # === DECADE DISTRIBUTION ===
    decades = Counter(p['year'] // 10 * 10 for p in posts)
    for decade, count in sorted(decades.items()):
        add_fact(
            'quirk',
            f"The {decade}s saw {count} posts published on the blog.",
            posts_sorted[-1]['link']
        )

    # === CONSECUTIVE POSTING STREAKS ===
    dates = sorted(set(p['date_obj'].date() for p in posts))
    max_streak = 1
    current_streak = 1
    streak_start = dates[0]
    best_streak_start = dates[0]

    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
                best_streak_start = streak_start
        else:
            current_streak = 1
            streak_start = dates[i]

    if max_streak >= 5:
        add_fact(
            'quirk',
            f"The longest consecutive posting streak was {max_streak} days, starting {best_streak_start.strftime('%B %d, %Y')}.",
            posts_sorted[-1]['link']
        )

    # === POSTS WITH SPECIFIC PATTERNS ===
    # Posts with equations/formulas
    equation_posts = [p for p in posts if has_equation(p.get('content', ''))]
    add_fact(
        'quirk',
        f"Approximately {len(equation_posts)} posts contain mathematical equations or formulas.",
        posts_sorted[-1]['link']
    )

    # Posts mentioning specific constants
    constants = [
        ('pi', 'π', '3.14159'),
        ('e', "Euler's number", '2.71828'),
        ('phi', 'golden ratio', '1.61803'),
        ('sqrt2', '√2', '1.41421'),
        ('sqrt3', '√3', '1.73205'),
        ('ln2', 'ln(2)', '0.69314'),
        ('gamma', 'Euler-Mascheroni', '0.57721'),
    ]

    for const_name, display_name, value in constants:
        const_posts = [p for p in posts if value in p['plain_content'] or display_name.lower() in p['plain_content'].lower()]
        if const_posts:
            add_fact(
                'constant',
                f"The constant {display_name} ({value}...) appears in {len(const_posts)} posts.",
                const_posts[0]['link']
            )

    # === POSTS BY HOUR OF DAY ===
    hour_counts = Counter(p['date_obj'].hour for p in posts)
    for hour, count in hour_counts.most_common():
        time_str = f"{hour:02d}:00"
        am_pm = "AM" if hour < 12 else "PM"
        hour_12 = hour % 12 or 12
        add_fact(
            'quirk',
            f"{count} posts were published at {hour_12}:00 {am_pm}.",
            posts_sorted[-1]['link']
        )

    # === WORD COUNT DISTRIBUTION ===
    word_counts = [p.get('word_count', 0) for p in posts]
    avg_word_count = sum(word_counts) / len(word_counts)
    add_fact(
        'quirk',
        f"The average blog post is {avg_word_count:.0f} words long.",
        posts_sorted[-1]['link']
    )

    # Posts in specific word count ranges
    ranges = [(0, 100), (100, 200), (200, 300), (300, 500), (500, 750), (750, 1000), (1000, 1500), (1500, 2000), (2000, 5000)]
    for low, high in ranges:
        range_posts = [p for p in posts if low <= p.get('word_count', 0) < high]
        if range_posts:
            add_fact(
                'quirk',
                f"{len(range_posts)} posts are between {low} and {high} words long.",
                posts_sorted[-1]['link']
            )

    # === SLUG PATTERNS ===
    # Longest slugs
    posts_by_slug_len = sorted(posts, key=lambda p: len(p.get('slug', '')), reverse=True)
    for post in posts_by_slug_len[:10]:
        add_fact(
            'quirk',
            f"The post \"{post['plain_title']}\" has one of the longest URL slugs at {len(post.get('slug', ''))} characters.",
            post['link'],
            post['date'],
            post['slug']
        )

    # Shortest slugs
    for post in posts_by_slug_len[-10:]:
        if len(post.get('slug', '')) <= 10:
            add_fact(
                'quirk',
                f"The post \"{post['plain_title']}\" has a short URL slug: '{post.get('slug', '')}'.",
                post['link'],
                post['date'],
                post['slug']
            )

    # === RELATED POSTS CHAINS ===
    # Posts that reference each other
    posts_with_links = [(p, re.findall(r'johndcook\.com/blog/\d{4}/\d{2}/\d{2}/([^/"]+)', p.get('content', ''))) for p in posts]
    for post, referenced_slugs in posts_with_links:
        if len(referenced_slugs) >= 3:
            add_fact(
                'quirk',
                f"\"{post['plain_title']}\" references {len(referenced_slugs)} other blog posts.",
                post['link'],
                post['date'],
                post['slug']
            )

    # === ANNIVERSARY FACTS ===
    # Find posts that happened exactly N years ago from a recent post
    recent_posts = [p for p in posts if p['year'] >= 2020]
    for recent in recent_posts[:50]:
        for years_ago in [5, 10, 15]:
            anniversary_posts = [p for p in posts
                               if p['month'] == recent['month']
                               and p['day'] == recent['day']
                               and p['year'] == recent['year'] - years_ago]
            if anniversary_posts:
                old_post = anniversary_posts[0]
                add_fact(
                    'otd',
                    f"\"{recent['plain_title']}\" ({recent['year']}) was published exactly {years_ago} years after \"{old_post['plain_title']}\" ({old_post['year']}).",
                    recent['link'],
                    recent['date'],
                    recent['slug']
                )

    return facts


def main():
    print("Loading posts...")
    posts = load_posts()
    print(f"Loaded {len(posts)} posts")

    print("Generating facts...")
    facts = generate_facts(posts)
    print(f"Generated {len(facts)} facts")

    # Write to CSV
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'type', 'fact', 'source_link', 'date', 'slug'])
        writer.writeheader()
        for fact in facts:
            writer.writerow(fact)

    print(f"Done! Output: {OUTPUT_FILE}")
    print(f"Total facts: {len(facts)}")

    # Summary by type
    type_counts = Counter(f['type'] for f in facts)
    print("\nFacts by type:")
    for t, c in type_counts.most_common():
        print(f"  {t}: {c}")


if __name__ == '__main__':
    main()
