# A Guide to the Book's Data

These files let you inspect selected archive measurements and repeat the calculations that
use them. You can follow a question from the book into a small table, or run the supplied
Python checker. You do not need the book's working repository.

Use this guide with the eight files in data, source-hashes.json and check-reader-evidence.py.
No download address is assumed here. The [unit guide](unit-to-file.md) identifies the relevant
file for each supported book section; the [data dictionary](data-dictionary.md) explains every
field.

## Start With a Question

- How did the account totals or prose-length distribution arise? Open archive-post-measures.csv.
- Which posts form the link comparisons? Open archive-link-pairs.csv.
- Which references were counted as Knuth or resolved as a particular Lewis? Open name-reference-posts.csv.
- What changed between saved versions? Start with changed-records.csv, then version-examples.json.
- How do the selected numerical examples work? Open numerical-examples.json and the checker.

CSV files are UTF-8 text with a header row. JSON files retain nested records and explanatory
limits. IDs identify posts; they are not ranks. Preserve hash strings and long integer/decimal
strings as text rather than rounding them in a spreadsheet.

## What the Dates Mean

The archive contains posts with a site-local publication timestamp before November 1, 2026
at midnight. Its capture ran on November 1 from 06:22:44 to 06:25:52 UTC. The date fields in
the CSVs describe publication, not retrieval or link insertion. Site-local timestamps have
no offset in these files; do not assign them a permanent UTC offset.

The capture was sequential, not an instantaneous historical copy. A current public URL can
show later changes. In version-examples.json, publication, modification and retrieval fields
are separate. The earlier collection's exact retrieval time is unknown. A blank or null
value means what the dictionary specifies; it does not mean zero or an observed absence.

## Run the Checks

Keep this structure, with the filenames unchanged. The enclosing folder can have any name:

    package-folder/
      check-reader-evidence.py
      source-hashes.json
      data/
        archive-post-measures.csv
        archive-link-pairs.csv
        variance-resource-sources.csv
        name-reference-posts.csv
        changed-records.csv
        archive-summary.json
        numerical-examples.json
        version-examples.json

Use Python 3.10 or later; the script uses only its standard library. From that folder, run:

    python3 --version
    python3 check-reader-evidence.py

Use ordinary Python execution, without -O or PYTHONOPTIMIZE: the checks use assertions.
No package installation, account, repository import or network connection is needed.
The directory must be writable because the script creates or replaces checks.json.

A successful run prints a JSON report with status set to passed and writes the same report
to checks.json. The report names the scope checked and what was not reproduced. An assertion
or other exception is a failure to complete the check, not a partial pass. If a file hash
fails, first verify that you have the matching, unmodified set of files; do not change the
expected hash merely to make the check pass.

## What a Pass Establishes

The script reaggregates recorded post measurements, selected link pairs, name assignments
and changed-field lists. It also checks the specified exponential-sum phase and path,
Kumaraswamy candidate gaps and total variation, scalar inverse-CDF examples, sequential
binary64 variance arithmetic and the selected harmonic-term difference.

This is **aggregation and selected calculation**, not a repeat of the original extraction.
The tables do not contain the full HTML corpus. They therefore cannot, by themselves,
reconstruct a historical page or rerun every prose-token, link or name-extraction decision.
The name identities are supplied assignments, not a new automated identity inference.

The numerical checker accepts the retained density-crossing candidates; it does not prove
that every crossing was found or find a globally best fit. Small floating-point residuals
do not prove exact closure; the exponential-sum argument also uses exact phase identities.
Some stored diagnostic values come from earlier checks and are not recomputed by this script.
No third-party application, complete harmonic-number program or historical audio is executed.

The script's hash check detects differences from the supplied data files. It does not make
the underlying observations true, authenticate a live website, or supply the missing raw
sources. The book's methods appendix supplies the population definitions and interpretation
limits needed to read these results.
