"""Check the selected reader tables/examples using only this folder and Python's library."""

import cmath
import csv
import hashlib
import json
import math
import statistics
from collections import Counter
from datetime import date
from fractions import Fraction
from itertools import pairwise
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name: str) -> dict:
    return json.loads((HERE / "data" / name).read_text(encoding="utf-8"))


def rows(name: str) -> list[dict]:
    with (HERE / "data" / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def quantile(values: list[int], probability: float) -> float:
    ordered = sorted(values)
    at = (len(ordered) - 1) * probability
    lo = int(at)
    return ordered[lo] + (ordered[min(lo + 1, len(ordered) - 1)] - ordered[lo]) * (at - lo)


def main() -> None:
    provenance = json.loads((HERE / "source-hashes.json").read_text(encoding="utf-8"))
    for path, expected in provenance["outputs"].items():
        assert hashlib.sha256((HERE / path).read_bytes()).hexdigest() == expected
    posts = rows("archive-post-measures.csv")
    assert len(posts) == len({p["post_id"] for p in posts}) == 5563
    assert Counter(p["account"] for p in posts) == {"1": 5522, "8": 41}
    windows = {}
    for year in [2025, 2026]:
        selected = [p for p in posts if f"{year}-01-01" <= p["publication_timestamp"][:10]
                    <= f"{year}-10-31"]
        windows[year] = dict(Counter(p["account"] for p in selected))
        assert (date(year, 10, 31) - date(year, 1, 1)).days + 1 == 304
    assert windows == {2025: {"1": 300, "8": 18}, 2026: {"1": 296, "8": 6}}
    values = [int(p["prose_words"]) for p in posts if p["account"] == "1"]
    assert (quantile(values, .25), statistics.median(values), quantile(values, .75)) == (147, 267, 409)
    assert sum(v >= 1000 for v in values) == 32
    assert next(p["prose_words"] for p in posts if p["post_id"] == "627") == "85"
    edges = rows("archive-link-pairs.csv")

    def cohort(name: str) -> list[dict]:
        return [e for e in edges if name in e["cohorts"].split(";")]

    assert len({(e["source_id"], e["target_url"]) for e in edges}) == len(edges)
    recent = cohort("2026_matched")
    decade = [e for e in recent if date.fromisoformat(e["target_date"][:10])
              <= date.fromisoformat(e["source_date"][:10]).replace(year=2016)]
    assert (len(recent), len(decade), len({e["source_id"] for e in decade}),
            len({e["target_id"] for e in decade})) == (647, 59, 47, 52)
    for name, count, years in [("chart_announcement", 1, 1), ("chart_reference", 42, 16),
                               ("floating_point", 47, 14), ("chart_legacy", 5, 4)]:
        selected = cohort(name)
        assert len({e["source_id"] for e in selected}) == count
        assert len({e["source_date"][:4] for e in selected}) == years
    canonical_ids = {e["source_id"] for e in cohort("chart_reference")}
    assert {e["source_id"] for e in cohort("chart_legacy")} <= canonical_ids
    assert not canonical_ids & {e["source_id"] for e in cohort("chart_announcement")}
    resources = rows("variance-resource-sources.csv")
    assert len(resources) == len({p["source_id"] for p in resources}) == 15
    assert sum(int(p["running_variance"]) for p in resources) == 11
    assert sum(int(p["higher_moments"]) for p in resources) == 7
    assert sum(p["running_variance"] == p["higher_moments"] == "1" for p in resources) == 3
    assert len({p["publication_timestamp"][:4] for p in resources}) == 9
    names = rows("name-reference-posts.csv")
    assert Counter(p["query"] for p in names) == {"Knuth": 61, "Lewis": 42}
    assert len({(p["query"], p["post_id"]) for p in names}) == 103
    lewis = Counter(p["resolved_person"] for p in names if p["query"] == "Lewis")
    assert sorted(lewis.values()) == [1, 1, 1, 1, 1, 2, 4, 8, 23]
    assert lewis["C. S. Lewis"] == 23
    changed = rows("changed-records.csv")
    fields = Counter(field for p in changed for field in p["changed_fields"].split(";"))
    assert len(changed) == len({p["post_id"] for p in changed}) == 148
    assert fields == {"modified": 127, "content": 117, "tags": 19, "excerpt": 14,
                      "categories": 14, "title": 1}
    assert sum(p["baseline_body_sha256"] != p["current_body_sha256"] for p in changed) == 117
    summary = read("archive-summary.json")
    assert len(set(summary["added_ids"])) == 330 and 5233 + 330 == len(posts)
    examples = read("numerical-examples.json")
    phase = examples["exponential_sum"]
    denominator = phase["phase_denominator"]
    residues = [(119*n + 170*n*n + 70*n*n*n) % denominator for n in range(1190)]
    assert all((residues[(n+119) % 1190]-residues[n]) % 1190 == 1071 for n in range(1190))
    proper_divisors = [d for d in range(1,1190) if 1190 % d == 0]
    assert all(any(residues[(n+d)%1190] != residues[n] for n in range(1190)) for d in proper_divisors)
    for n in range(1190):
        f = lambda k: Fraction(k,10)+Fraction(k*k,7)+Fraction(k*k*k,17)
        assert f(n+119)-f(n) == 21*n*n+2533*n+101161+Fraction(9,10)
    q = cmath.exp(2j*math.pi*.9)
    path = [0j]
    for n in range(3,12003):
        path.append(path[-1]+cmath.exp(2j*math.pi*residues[n%1190]/1190))
    center = path[119]/(1-q)
    assert abs(center-complex(*phase["rotation_center"])) < 1e-11
    assert abs(path[1190]) < 1e-10
    assert abs(path[12000]-path[100]) < 1e-10
    assert abs(path[12000]-complex(*phase["end_of_12000_steps"])) < 1e-10
    assert max(abs(path[j+119]-path[119]-q*path[j]) for j in range(1191)) < 1e-10
    # Exact residue/orbit facts support closure; these residual checks are not a proof by rounding.
    gaps = []
    total_variations = []
    for item in examples["kumaraswamy"]:
        x = item["retained_cdf_extremum_x"]
        a, b = item["kumaraswamy_parameters"]
        alpha, beta = item["beta_parameters"]
        if (alpha, beta) == (.5, .5):
            beta_cdf = 2 / math.pi * math.asin(math.sqrt(x))
            beta_density = 1 / (math.pi * math.sqrt(x * (1 - x)))
        else:
            assert (alpha, beta) == (5, 3)
            beta_cdf = 21 * x**5 - 35 * x**6 + 15 * x**7
            beta_density = 105 * x**4 * (1 - x)**2
        kum_cdf = -math.expm1(b * math.log1p(-x**a))
        gap = abs(kum_cdf - beta_cdf)
        assert math.isclose(gap, item["retained_refined_cdf_gap"], abs_tol=3e-14)
        kum_density = a * b * x**(a - 1) * (1 - x**a)**(b - 1)
        assert abs(kum_density - beta_density) < 1e-10
        stationary = ((a - 1) / (a * b - 1))**(1 / a)
        assert math.isclose(stationary, item["kumaraswamy_stationary_x"], abs_tol=2e-14)
        crossings = item["density_crossings"]
        bounds = [0.0, *crossings, 1.0]
        differences = []
        for value in bounds:
            if value in (0.0,1.0):
                differences.append(0.0)
                continue
            target = (2/math.pi*math.asin(math.sqrt(value)) if alpha == .5
                      else 21*value**5-35*value**6+15*value**7)
            candidate = -math.expm1(b*math.log1p(-value**a))
            differences.append(candidate-target)
        total_variation = sum(abs(right-left) for left,right in pairwise(differences))/2
        assert math.isclose(total_variation,item["retained_total_variation"],abs_tol=3e-14)
        total_variations.append(total_variation)
        gaps.append(gap)
    small = examples["kumaraswamy_small_u"]
    u, a, b = small["u"], small["a"], small["b"]
    direct = (1 - (1 - u)**(1 / b))**(1 / a)
    stable = (-math.expm1(math.log1p(-u) / b))**(1 / a)
    assert math.isclose(direct, small["naive_quantile"], abs_tol=1e-16)
    assert math.isclose(stable, float(small["high_precision_reference"]), rel_tol=1e-14)
    variance = examples["variance"]
    values = variance["inputs"]
    total = squares = 0.0
    for x in values:
        total += x
        squares += x * x
    assert squares == variance["float_sum_squares"]
    assert (squares - total * total / 3) / 2 == 0
    assert sum(int(x)**2 for x in values) == int(variance["exact_sum_squares"])
    mean = values[0]
    m2 = 0.0
    for count, x in enumerate(values[1:], start=2):
        delta = x - mean
        mean += delta / count
        m2 += delta * (x - mean)
    assert m2 / 2 == 1
    normal = examples["normal_inverse"]
    c, d = (examples["normal_inverse_coefficients"][key] for key in ["c", "d"])
    t = math.sqrt(-2 * math.log(normal["p"]))
    approximate = -(t - ((c[2] * t + c[1]) * t + c[0])
                    / (((d[2] * t + d[1]) * t + d[0]) * t + 1))
    assert math.isclose(approximate, normal["lower_tail_approximation"], abs_tol=1e-15)
    assert math.isclose(.5 * math.erfc(-approximate / math.sqrt(2)),
                        normal["reference_cdf_at_approximate_lower_cutoff"], abs_tol=1e-15)
    version = read("version-examples.json")
    assert [e["display_line"][-5:] for e in version["harmonic_code_lines"]] == ["n**3)", "n**2)"]
    assert Fraction(1, 12 * 1000**2) - Fraction(1, 12 * 1000**3) == Fraction(333, 4000000000)
    result = {
        "status": "passed", "scope": "Aggregation of selected recorded measurements and bounded examples",
        "archive_posts": len(posts), "selected_link_pairs": len(edges),
        "name_query_post_rows": len(names), "changed_records": len(changed),
        "exponential_sum_period": denominator, "cdf_gaps_at_retained_candidates": gaps,
        "total_variations_from_retained_crossings": total_variations,
        "not_reproduced": ["Raw HTML extraction", "Historical website state", "Complete root search",
                           "Third-party runtimes", "Full harmonic program or historical audio"],
    }
    (HERE / "checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
