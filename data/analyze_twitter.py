import json
import re
from collections import Counter

posts = []
with open('/Users/owen.d.goode/Desktop/cookbook/data/johndcook_posts_enriched.jsonl', 'r') as f:
    for line in f:
        try:
            posts.append(json.loads(line))
        except:
            pass

print(f'Loaded {len(posts)} posts')

# Find all twitter URLs
all_twitter = Counter()
for p in posts:
    content = str(p.get('content', '')) + ' ' + str(p.get('text', ''))
    urls = re.findall(r'twitter\.com/([A-Za-z0-9_]+)', content)
    for u in urls:
        ul = u.lower()
        if ul not in ['widgets', 'hashtag', 'share', 'intent', 'search', 'home']:
            all_twitter[ul] += 1

print('\nALL TWITTER ACCOUNTS LINKED FROM BLOG:')
print('=' * 50)
for acc, count in all_twitter.most_common(40):
    print(f'  @{acc}: {count} links')

# Identify topic-based accounts (likely Johns)
topic_keywords = ['fact', 'tip', 'daily', 'symbol', 'vocab']
topic_accounts = [(a, c) for a, c in all_twitter.most_common(100)
                  if any(k in a for k in topic_keywords)]

print(f'\nTOPIC-BASED ACCOUNTS (likely Johns): {len(topic_accounts)}')
for acc, count in sorted(topic_accounts, key=lambda x: -x[1]):
    print(f'  @{acc}: {count}')
