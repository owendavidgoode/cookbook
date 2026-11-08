# From a Book Section to Its Data

Unit IDs and note numbers identify sections without requiring final page numbers. “Direct”
means that a current source note refers to the file. “Supporting” means the file supplies
aggregation inputs for that section or its methods; it is not an additional citation claim.
This is a selected companion, not a dataset for every example in the book.

| Unit and question | File or JSON section | Connection |
| --- | --- | --- |
| A1 — One Address, More Than One Voice: accounts and matched publication windows | archive-post-measures.csv; archive-summary.json | Supporting; methods M1–M2 |
| A2 — What the Word Count Leaves Out: prose lengths | archive-post-measures.csv | Supporting; note A2.2 and method M3 |
| A2 — announcement versus reference | archive-link-pairs.csv | Direct, A2.3; method M4 |
| A3 — An Explanation You Can Return To: recent-to-old pairs and the floating-point article | archive-link-pairs.csv | Direct, A3.4; method M4 |
| A3 — the separate two-resource census | variance-resource-sources.csv | Supporting; note A3.5 and method M4 |
| A4 — People in the References: Knuth and Lewis sets | name-reference-posts.csv | Direct, A4.3 and A4.6; method M5 |
| A5 — An Archive That Keeps Changing: added IDs and field differences | archive-summary.json; changed-records.csv | Changed-record table direct in A5.3; methods M1/M6 |
| A5 — the harmonic-code and audio-counter examples | version-examples.json | Direct, A5.5 |
| F3 — A Date Drawn in Steps | numerical-examples.json → exponential_sum | Direct, F3.2 |
| F6 — A Convenient Substitute | numerical-examples.json → kumaraswamy and kumaraswamy_small_u | Direct, F6.2–F6.3 |
| F7 — When a Reader Is Right | numerical-examples.json → variance | Direct, F7.2 |
| F8 — The Work Between a Formula and a Function | numerical-examples.json → normal_inverse and normal_inverse_coefficients | Direct, F8.2 |

check-reader-evidence.py checks these tables and selected examples together. It is directly
referenced in F3.2, F6.3, F7.2 and F8.2. source-hashes.json supplies the eight data-file hashes
that the checker verifies before calculating; it is a supporting manifest, not a ninth
data table.

## Counting Without Adding Overlapping Groups

In archive-link-pairs.csv, filter the cohorts field as a semicolon-separated list. A single
row can belong to several cohorts. The file is their union, so do not add cohort totals and
call the result a count of distinct pairs. Distinct source posts and distinct pairs are also
different units.

The five exact cohort labels are:

| Label | Selected population |
| --- | --- |
| 2026_matched | Cook-account sources published in 2026, linked to a captured post |
| chart_announcement | Cook-account sources linked to announcement post 627 |
| chart_reference | Cook-account sources linked to the canonical distribution-chart reference |
| chart_legacy | Cook-account sources linked to the separate legacy .html chart address |
| floating_point | Cook-account sources linked to “Anatomy of a floating point number,” post 1956 |

The legacy chart's sources also appear among the canonical reference's sources; the URLs
remain distinct destinations. A standalone reference has no target post ID or publication
date in this table. That absence does not establish that the reference has no date.

In name-reference-posts.csv, one row is a query/post pair. Knuth and Lewis are query labels,
not two mutually exclusive sets of posts. resolved_person supplies the retained identification;
it does not grade influence or endorse every statement in the post.

In changed-records.csv, one row is a shared post ID with at least one changed field. Multiple
field names in a row are overlapping descriptions of that record. A changed body is not
automatically a changed argument.
