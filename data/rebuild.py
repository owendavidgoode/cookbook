import csv
import sys
import os

# Get directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Read all current facts
facts = []
with open(os.path.join(SCRIPT_DIR, 'johndcook_calendar_365.csv'), 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        facts.append(row)

# Read new facts
new_facts = []
with open(os.path.join(SCRIPT_DIR, 'new_deep_analysis_facts.csv'), 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_facts.append(row)

# Group by type
by_type = {}
for f in facts:
    t = f['type']
    if t not in by_type:
        by_type[t] = []
    by_type[t].append(f)

# Print current dist
print("CURRENT:")
for t in sorted(by_type.keys(), key=lambda x: len(by_type[x]), reverse=True):
    print(f"  {t}: {len(by_type[t])}")

# Remove facts
# Rarity: remove gibberish (no 'word','letter','english','dictionary','pangram','lipogram')
rarity_keep = []
rarity_remove = []
for f in by_type.get('rarity', []):
    txt = f['fact'].lower()
    if any(w in txt for w in ['word','letter','english','dictionary','pangram','lipogram','sentence','language','text']):
        rarity_keep.append(f)
    else:
        rarity_remove.append(f)

print(f"\nRarity: keep {len(rarity_keep)}, remove {len(rarity_remove)}")
rarity_final = rarity_keep + rarity_remove[25:]  # Remove first 25 gibberish
print(f"Rarity final: {len(rarity_final)}")

# OTD: remove 7 least interesting (no theorem, formula, crypto, recent years)
otd_scored = []
for f in by_type.get('otd', []):
    score = 0
    txt = f['fact'].lower()
    if any(w in txt for w in ['theorem','formula','function','equation','algorithm','crypto','bitcoin','fractal']):
        score += 2
    if any(w in txt for w in ['highlight','posts','help','monthly','carnival']):
        score -= 2
    if f.get('date','').startswith('202'):
        score += 1
    otd_scored.append((score, f))

otd_scored.sort(key=lambda x: x[0])
otd_final = [f for s,f in otd_scored[7:]]
print(f"OTD: keeping {len(otd_final)} (removed 7)")

# Quirk: remove first 10
quirk_final = by_type.get('quirk', [])[10:]
print(f"Quirk: keeping {len(quirk_final)} (removed 10)")

# Build new list
result = []
result.extend(rarity_final)
result.extend(otd_final)
result.extend(quirk_final)

# Add unchanged categories
for t in by_type:
    if t not in ['rarity','otd','quirk']:
        result.extend(by_type[t])

print(f"\nTotal kept from original: {len(result)}")

# Add new facts
for nf in new_facts:
    result.append({
        'id': '0',
        'type': nf['type'],
        'fact': nf['fact'],
        'source_link': 'https://www.johndcook.com/blog/',
        'date': '',
        'slug': ''
    })

print(f"After adding new: {len(result)}")

# Renumber
for i, f in enumerate(result, 1):
    f['id'] = str(i)

# Count final
final_dist = {}
for f in result:
    t = f['type']
    final_dist[t] = final_dist.get(t, 0) + 1

print("\nFINAL:")
for t in sorted(final_dist.keys(), key=lambda x: final_dist[x], reverse=True):
    print(f"  {t}: {final_dist[t]}")

# Write
with open(os.path.join(SCRIPT_DIR, 'johndcook_calendar_365.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id','type','fact','source_link','date','slug'])
    writer.writeheader()
    writer.writerows(result)

print(f"\nWrote {len(result)} facts")
