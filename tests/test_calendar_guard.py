import csv
import hashlib
from pathlib import Path

from cookbook import paths


CANONICAL_CALENDAR = paths.data_path("johndcook_calendar_365.csv")
CANONICAL_HASH = paths.data_path("calendar", "final", "canonical.sha256")


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def test_calendar_checksum_matches_reference() -> None:
    expected = Path(CANONICAL_HASH).read_text(encoding="utf-8").split()[0]
    assert _sha256(CANONICAL_CALENDAR) == expected


def test_calendar_has_expected_shape() -> None:
    rows = list(csv.DictReader(CANONICAL_CALENDAR.open(encoding="utf-8")))
    assert len(rows) == 365
    required_fields = {"id", "type", "fact", "source_link", "date", "slug"}
    assert required_fields.issubset(set(rows[0].keys()))

    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids)), "Duplicate IDs found in calendar CSV."

    facts = [row["fact"].strip() for row in rows]
    assert len(facts) == len(set(facts)), "Duplicate fact texts found in calendar CSV."
