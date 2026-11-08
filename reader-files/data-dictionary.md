# Data Dictionary

Field names below match the supplied files. Dots indicate nested JSON objects; [] means each object in an array. CSV types describe how to interpret text cells. JSON numbers are stored numeric values; exact integer/rational strings and high-precision decimal strings retain their distinct meanings.

Empty CSV target fields and JSON nulls are explained explicitly. An absent key is not silently replaced with zero. All hashes are provenance checks, not proof of truth or live-site authenticity.

## archive-link-pairs.csv

739 records. Empty fields: target_id, target_date.

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| cohorts | string list | semicolon-separated labels | Membership in one or more of the five cohorts defined in unit-to-file.md. Do not add overlapping cohort totals. |
| source_id | integer identifier | post ID | Cook-account source post; join to archive-post-measures.post_id. |
| source_date | timestamp string | site-local publication time | Source publication field, not link insertion or retrieval time. |
| source_url | string | public URL | Source post address. |
| target_id | integer identifier or empty | post ID | Captured target post ID when matched; empty for a standalone chart-reference destination. |
| target_date | timestamp string or empty | site-local publication time | Captured target post publication field; empty when the target is outside the post snapshot, not proof that it has no date. |
| target_url | string | normalized URL | Destination used by the pair count; protocol/www/trailing slash/fragment normalization is described in M4. The legacy chart URL is separate. |

## archive-post-measures.csv

5,563 records. No empty cells in this supplied table.

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| post_id | integer identifier | post ID | Stable post identifier used for joins, not a rank or publication-order position. |
| publication_timestamp | timestamp string | site-local publication time | Publication field in the capture; no UTC offset is supplied and this is not retrieval time. |
| account | integer code | current account ID | 1 denotes Cook; 8 denotes Wayne Joubert in this capture. It does not identify every quoted speaker. |
| prose_words | nonnegative integer | word-like tokens | Recorded visible-body measure under M3's exclusions; title and image alt text excluded. Zero is a measured count, not missing data. |
| source_url | string | public URL | Address of the cited source post; the live page can change after capture. |
| body_sha256 | string | SHA-256 hex digest | Hash of UTF-8 stored content HTML, not a hash of the live page or its raw HTTP response. |

## archive-summary.json

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| captured_posts | integer | post records | Size of the later captured collection. |
| baseline_posts | integer | post records | Size of the preserved first-edition research collection, not a claim about a printed edition's contents. |
| added_ids | array of integers | post IDs | IDs in the later collection but absent from the baseline. Novel to this comparison, not necessarily newly discovered by readers. |
| comparison_window | string | calendar definition | Matched January 1–October 31 windows; the years used by the checker are 2025 and 2026. |
| publication_cutoff_exclusive_site_local | timestamp string | site-local boundary | Posts must have publication timestamps strictly earlier than this value; equality is excluded. |
| capture_interval_utc | two timestamp strings | UTC start/end | Bulk retrieval interval. These strings omit an offset suffix, but the field explicitly identifies UTC. |
| scope | string | scope statement | Recorded measurements, not raw HTML or an instantaneous historical reconstruction. |

## changed-records.csv

148 records. No empty cells in this supplied table.

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| post_id | integer identifier | post ID | Stable post identifier used for joins, not a rank or publication-order position. |
| changed_fields | string list | semicolon-separated field names | Comparable fields that differ for this shared post ID: modified, content, tags, excerpt, categories or title. Counts overlap. |
| baseline_body_sha256 | string | SHA-256 hex digest | Hash of the baseline's stored content HTML; a body may match even when another field changed. |
| current_body_sha256 | string | SHA-256 hex digest | Hash of the later stored content HTML. Different bytes do not establish a substantive argument change. |
| source_url | string | public URL | Address of the cited source post; the live page can change after capture. |

## name-reference-posts.csv

103 records. No empty cells in this supplied table.

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| query | enum string | Knuth or Lewis | Query label under the M5 parsing rule; one row per query/post combination. |
| post_id | integer identifier | post ID | Stable post identifier used for joins, not a rank or publication-order position. |
| publication_timestamp | timestamp string | site-local publication time | Publication field in the capture; no UTC offset is supplied and this is not retrieval time. |
| resolved_person | string | identity label | Retained context-based identification. A supplied audit assignment, not a new inference by the checker or a measure of influence. |
| source_url | string | public URL | Address of the cited source post; the live page can change after capture. |

## numerical-examples.json

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| kumaraswamy[].label | string | case label | Identifies one of four comparisons: Cook's two cases or the reader-supplied alternatives. |
| kumaraswamy[].beta_parameters | two numbers | dimensionless [alpha,beta] | Ordered shape parameters of the target beta distribution. |
| kumaraswamy[].kumaraswamy_parameters | two numbers | dimensionless [a,b] | Ordered shape parameters of the compared Kumaraswamy distribution; stored numeric approximations where applicable. |
| kumaraswamy[].stationary_kind | enum string | minimum or mode | Type of interior stationary point of the density in this case; U-shaped minima must not be called modes. |
| kumaraswamy[].kumaraswamy_stationary_x | number | x on [0,1] | Numerical location of that density stationary point. |
| kumaraswamy[].retained_refined_cdf_gap | number | probability difference | Absolute CDF gap at the retained candidate extremum; multiply by 100 for percentage points, not percent of density height. |
| kumaraswamy[].retained_cdf_extremum_x | number | x on [0,1] | Retained candidate location of the displayed CDF gap. |
| kumaraswamy[].density_crossings | array of numbers | x on [0,1] | Candidate equal-density locations from the earlier numerical search. Exhaustiveness is not proved. |
| kumaraswamy[].retained_total_variation | number | dimensionless distance | Reported total-variation comparison from those candidate roots; not an optimal-fit certificate. |
| kumaraswamy[].numerical_search_limit | string | method/limit statement | Documents the earlier grid/root refinement. The reader checker consumes these roots rather than repeating that search. |
| kumaraswamy_small_u.u | number | probability | The single uniform-probability input used for the cancellation example. |
| kumaraswamy_small_u.a | number | dimensionless shape | Kumaraswamy first parameter for the small-u example. |
| kumaraswamy_small_u.b | number | dimensionless shape | Kumaraswamy second parameter for the small-u example. |
| kumaraswamy_small_u.naive_quantile | number | x on [0,1] | Direct evaluation of the inverse formula at the selected input. |
| kumaraswamy_small_u.log1p_expm1_quantile | number | x on [0,1] | Evaluation using log1p/expm1 to reduce cancellation; one-input result, not an all-input guarantee. |
| kumaraswamy_small_u.high_precision_reference | decimal string | x on [0,1] | Retained high-precision numerical reference. String encoding preserves digits; it is still an approximation. |
| kumaraswamy_small_u.naive_relative_error | decimal string | fractional error | Retained absolute relative error of the direct result; multiply by 100 for percent. Not an error bound. |
| kumaraswamy_small_u.log1p_expm1_relative_error | decimal string | fractional error | Retained relative error of the alternative evaluation. |
| kumaraswamy_small_u.limit | string | scope statement | Single deterministic example; endpoints and general stability require separate treatment. |
| variance.inputs | array of numbers | observation units | Three exactly representable input observations for this constructed example. |
| variance.exact_sum_squares | integer string | squared observation units | Exact integer sum; string encoding protects its final digits from floating-point conversion. |
| variance.float_sum_squares | number | squared observation units | Sum produced after sequential binary64 squaring/addition; different from rounding the exact total once. |
| variance.naive_sample_variance | number | squared observation units | Raw-sum sample variance under the specified evaluation order. |
| variance.welford_states | array of triples | [count,mean,M2] | Successive count, mean in observation units, and centered sum in squared units; M2 is not yet variance. |
| variance.welford_sample_variance | number | squared observation units | Final M2 divided by n−1 for the three-observation sample. |
| normal_inverse.purpose | string | scope statement | Explains the single-input calculation and what it does not certify. |
| normal_inverse.p | number | probability | Input cumulative probability for the lower cutoff; also the upper-tail magnitude used by symmetry in this example. |
| normal_inverse.normal_mean | number | standard-normal coordinates | Reference distribution mean, zero. |
| normal_inverse.normal_standard_deviation | number | standard-normal coordinates | Reference distribution standard deviation, one. |
| normal_inverse.t | number | dimensionless auxiliary variable | sqrt(−2 ln p) for this input; unrelated to the randomized-response parameter t elsewhere in the book. |
| normal_inverse.numerator | number | dimensionless | Evaluated c0+c1*t+c2*t² in the rational correction. |
| normal_inverse.denominator | number | dimensionless | Evaluated 1+d0*t+d1*t²+d2*t³ in the rational correction. |
| normal_inverse.upper_tail_approximation | number | standard-normal cutoff | Positive approximate upper-tail cutoff. |
| normal_inverse.lower_tail_approximation | number | standard-normal cutoff | Negative cutoff after the selected symmetry/sign branch. |
| normal_inverse.reference_lower_cutoff | number | standard-normal cutoff | Retained numerical reference for the inverse CDF at p. |
| normal_inverse.erfc_bisection_lower_cutoff | number | standard-normal cutoff | Earlier bisection cross-check; the reader script does not repeat that bisection. |
| normal_inverse.absolute_cutoff_error_at_this_input | number | standard-normal coordinates | Absolute difference at this input, not a uniform approximation bound. |
| normal_inverse.reference_cdf_at_reference_cutoff | number | probability | Reference CDF evaluated at its reference cutoff. |
| normal_inverse.reference_cdf_at_approximate_lower_cutoff | number | probability | Reference CDF evaluated at the approximate lower cutoff; checked by the reader script. |
| normal_inverse.reference_cdf_if_wrong_positive_sign_kept | number | probability | Counterfactual diagnostic if the sign branch were omitted; not an output to adopt. |
| normal_inverse.implementation | string | implementation scope | Specifies the Python double-precision transcription and excludes third-party runtime execution. |
| normal_inverse_coefficients.c | three numbers | [c0,c1,c2] | Numerator coefficients in ascending powers of t. |
| normal_inverse_coefficients.d | three numbers | [d0,d1,d2] | Denominator coefficients multiplying t,t²,t³ respectively; the constant is 1. |
| limits | array of strings | scope statements | Shared limits on approximation, evaluation order and single-input checks. |
| exponential_sum.post_id | integer identifier | post ID | Cook source post 28835; identifies the particular dated construction. |
| exponential_sum.phase | string | formula in turns | f(n) and its rational-polynomial form; each step is exp(2πi f(n)). |
| exponential_sum.sample_range.n_first | integer | step index n | First source-code step index, inclusive. |
| exponential_sum.sample_range.n_last | integer | step index n | Last source-code step index, inclusive. |
| exponential_sum.sample_range.count | integer | steps | Number of source-code steps; not the number of distinct points in the closed pattern. |
| exponential_sum.exact_minimal_phase_period | integer | steps | Minimal period of the phase modulo one/step directions, not periodicity of the unbounded polynomial. |
| exponential_sum.shift | integer | steps | Block shift producing a constant rotation modulo whole turns. |
| exponential_sum.exact_shift_phase_mod_one | rational string | turns | Exact fractional phase change for that shift; 9/10 turn is equivalent to 36 degrees clockwise. |
| exponential_sum.closure_argument | string | mathematical explanation | Finite geometric-series argument for exact block closure; separate from numerical residuals. |
| exponential_sum.block_1190_float_residual | number | unit-step length units | Recorded magnitude of the floating closure residual; not proof of exact zero. |
| exponential_sum.affine_block_relation | string | formula | Relation between partial sums, with P(0)=0 specified. |
| exponential_sum.affine_block_relation_max_float_residual | number | unit-step length units | Earlier maximum numerical residual for the affine relation; not a universal error bound. |
| exponential_sum.rotation_center | two numbers | [real,imaginary] coordinates | Center of rotation in the unit-step plane; distinct from starting vertex P(0). |
| exponential_sum.source_direct_vs_reduced_phase_max_path_difference | number | unit-step length units | Earlier maximum discrepancy between direct and modular-reduced phase evaluation. This comparison is not rerun by the reader checker. |
| exponential_sum.step_integer_numerator_coefficients | three integers | coefficients of [n,n²,n³] | Ordered coefficients 119,170,70 before division by phase_denominator; there is no listed constant term. |
| exponential_sum.phase_denominator | integer | turn divisor | Denominator used for exact integer-residue phase reduction. |
| exponential_sum.scope | string | scope statement | Limits the example to the stated date polynomial/range, without general-date or winding-number claims. |
| exponential_sum.end_of_12000_steps | two numbers | [real,imaginary] coordinates | Retained endpoint of the full plotted run; it is not the closed-period endpoint. |

## variance-resource-sources.csv

15 records. No empty cells in this supplied table.

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| source_id | integer identifier | post ID | Unique Cook-account source post in the two-resource census. |
| publication_timestamp | timestamp string | site-local publication time | Publication field in the capture; no UTC offset is supplied and this is not retrieval time. |
| source_url | string | public URL | Address of the cited source post; the live page can change after capture. |
| running_variance | integer flag | 0 or 1 | 1 means a captured qualifying link to the running-variance reference; 0 means no qualifying link under that rule. |
| higher_moments | integer flag | 0 or 1 | 1 means a captured qualifying link to the higher-moments reference. Both flags can be 1; this is an intersection, not a second person. |

## version-examples.json

| Field | Type | Units or representation | Meaning |
| --- | --- | --- | --- |
| pairs[].post_id | integer identifier | post ID | Identifies one of the two compared Cook posts. |
| pairs[].title | string | source title | Title identifying the comparison. |
| pairs[].url | string | public URL | Current source address; not a historical snapshot URL. |
| pairs[].versions.baseline.body_sha256 | string | SHA-256 hex digest | Hash of the stored content HTML for this version. |
| pairs[].versions.baseline.published_site_local | timestamp string | site-local source field | Publication or modification field as named; not the exact time of each edit. |
| pairs[].versions.baseline.modified_site_local | timestamp string | site-local source field | Publication or modification field as named; not the exact time of each edit. |
| pairs[].versions.baseline.author_account | null | account ID | Baseline: not captured, not zero. Current: account 1 in these two records; not authorship of every sentence. |
| pairs[].versions.baseline.author_account_status | string | metadata status | Explicitly distinguishes unknown_not_captured from captured_current_assignment. |
| pairs[].versions.baseline.retrieval_time | null | unknown | The baseline fetch time is not established; do not substitute its publication/modification date. |
| pairs[].versions.baseline.retrieval_limit | string | scope statement | Explains the unavailable baseline retrieval time. |
| pairs[].versions.current.body_sha256 | string | SHA-256 hex digest | Hash of the stored content HTML for this version. |
| pairs[].versions.current.published_site_local | timestamp string | site-local source field | Publication or modification field as named; not the exact time of each edit. |
| pairs[].versions.current.modified_site_local | timestamp string | site-local source field | Publication or modification field as named; not the exact time of each edit. |
| pairs[].versions.current.author_account | integer code | account ID | Baseline: not captured, not zero. Current: account 1 in these two records; not authorship of every sentence. |
| pairs[].versions.current.author_account_status | string | metadata status | Explicitly distinguishes unknown_not_captured from captured_current_assignment. |
| pairs[].versions.current.capture.record_line | integer | one-based JSONL line | Locator in the preserved normalized post file, not a line in this reader file. |
| pairs[].versions.current.capture.record_line_sha256_without_newline | string | SHA-256 hex digest | Hash of that normalized JSONL record line without its newline; different object from the HTML body hash. |
| pairs[].versions.current.capture.raw_file | string | provenance path | Identifier of the retained raw response file. That raw file is not included or required by the reader checker; this is not a download link. |
| pairs[].versions.current.capture.raw_sha256 | string | SHA-256 hex digest | Hash of the raw response bytes, which can contain multiple posts. |
| pairs[].versions.current.capture.retrieved_at_utc | timestamp string | UTC retrieval time | Recorded request timestamp with explicit +00:00 offset. |
| harmonic_code_lines[].version | enum string | baseline or current | Which saved version supplied the selected line. |
| harmonic_code_lines[].pre_index_1_based | integer | one-based pre block | Ordinal of the preformatted block in the saved content. |
| harmonic_code_lines[].decoded_pre_line_1_based | integer | one-based line | Line within that decoded pre block. |
| harmonic_code_lines[].exact_line | string | code text | Selected line including its indentation; not a complete executable program. |
| harmonic_code_lines[].display_line | string | code text | Same selected line with leading indentation removed for display. |
| harmonic_code_lines[].character_range_in_decoded_pre | two integers | zero-based half-open character offsets | Start included, end excluded in the decoded pre text; not byte offsets or final book lines. |
| audio_counter_spans.baseline[].kind | enum string | span category | audio_element_id or numeric_query_counter; this names HTML markup, not an audio waveform. |
| audio_counter_spans.baseline[].exact_html_span | string | HTML text | The exact selected counter span in the stored body. |
| audio_counter_spans.baseline[].character_range_in_content | two integers | zero-based half-open character offsets | Location in the stored content string. Source content is not included in this compact file. |
| audio_counter_spans.current[].kind | enum string | span category | audio_element_id or numeric_query_counter; this names HTML markup, not an audio waveform. |
| audio_counter_spans.current[].exact_html_span | string | HTML text | The exact selected counter span in the stored body. |
| audio_counter_spans.current[].character_range_in_content | two integers | zero-based half-open character offsets | Location in the stored content string. Source content is not included in this compact file. |
| limits | array of strings | scope statements | Preserves unknown retrieval timing and limits on source-body/program/audio reproduction. |

## Supporting Manifest and Check Output

source-hashes.json supplies outputs, a mapping from the eight data-relative filenames to their SHA-256 strings. The checker verifies that mapping. The full provenance version also has inputs, mapping source identifiers to hashes, and scope, describing the selection. These extra fields are not required by the checker. A minimal reader manifest can contain outputs alone; no original source files are required.

The checker creates checks.json with status and scope strings; archive_posts, selected_link_pairs, name_query_post_rows and changed_records counts; exponential_sum_period in steps; cdf_gaps_at_retained_candidates and total_variations_from_retained_crossings in the same four-case order as kumaraswamy; and not_reproduced as a list of exclusions. It also prints this object. A passed result applies to the script’s selected checks, not every diagnostic field stored above.

The script recomputes selected quantities, including the reported CDF gaps/total variations from supplied candidates and the scalar approximations. It does not rerun the original high-precision root search, the normal-reference bisection, raw HTML extraction or the direct-versus-reduced full-path comparison. Stored reference values retain their role as references.
