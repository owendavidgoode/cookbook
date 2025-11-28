import json

from typer.testing import CliRunner

from cookbook.cli import app


def test_bot_validate_accepts_valid_facts(tmp_path) -> None:
    facts_path = tmp_path / "facts.json"
    facts_path.write_text(json.dumps([{"id": 1, "text": "short fact", "type": "test"}]))
    result = CliRunner().invoke(app, ["bot", "validate", "--facts-path", str(facts_path)])
    assert result.exit_code == 0


def test_bot_validate_rejects_long_fact(tmp_path) -> None:
    facts_path = tmp_path / "facts.json"
    long_text = "x" * 300
    facts_path.write_text(json.dumps([{"id": 1, "text": long_text, "type": "test"}]))
    result = CliRunner().invoke(app, ["bot", "validate", "--facts-path", str(facts_path)])
    assert result.exit_code != 0
