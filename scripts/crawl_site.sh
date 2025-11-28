#!/usr/bin/env bash
# Simple wrapper around wget to mirror a site for offline analysis.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/crawl_site.sh -u https://www.example.com [/blog/] [-o output_dir]

Mirrors the given URL with wget:
  - Follows links on the same domain only
  - Converts links for local browsing
  - Saves assets (CSS/JS/images)
  - Ignores robots.txt (assumes you have permission)

Options:
  -u  Root URL to crawl (required), e.g., https://www.johndcook.com/blog/
  -o  Output directory (default: data/crawl)

Examples:
  scripts/crawl_site.sh -u https://www.johndcook.com/blog/ -o data/johndcook-crawl
EOF
}

url=""
out_dir="data/crawl"

while getopts "u:o:h" opt; do
  case "${opt}" in
    u) url="${OPTARG}" ;;
    o) out_dir="${OPTARG}" ;;
    h) usage; exit 0 ;;
    *) usage; exit 1 ;;
  esac
done

if [[ -z "${url}" ]]; then
  usage
  exit 1
fi

if ! command -v wget >/dev/null 2>&1; then
  echo "Error: wget not found. Install wget and retry." >&2
  exit 1
fi

# Extract domain for --domains whitelist
domain="$(python3 - "$url" <<'PY'
import sys
from urllib.parse import urlparse

if len(sys.argv) < 2:
    sys.exit("Missing URL argument")
url = sys.argv[1]
parsed = urlparse(url)
host = parsed.netloc
if not host:
    sys.exit("Could not parse domain from URL: %s" % url)
print(host)
PY
)"

mkdir -p "${out_dir}"

echo "Crawling ${url}"
echo "Output directory: ${out_dir}"
echo "Domain allowlist: ${domain}"

wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  --execute robots=off \
  --wait=0.5 \
  --random-wait \
  --reject-regex ".*\\?(replytocom|utm_).*" \
  --directory-prefix="${out_dir}" \
  --domains="${domain}" \
  "${url}"

echo "Done. Local copy at ${out_dir}/${domain}"
