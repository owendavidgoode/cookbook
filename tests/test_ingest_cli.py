from typer.testing import CliRunner

from cookbook.cli import app


def test_ingest_help_lists_commands() -> None:
    result = CliRunner().invoke(app, ["ingest", "--help"])
    assert result.exit_code == 0
    assert "wp-api" in result.stdout
    assert "taxonomies" in result.stdout
    assert "enrich" in result.stdout
    assert "index" in result.stdout
