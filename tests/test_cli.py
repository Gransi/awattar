
from click.testing import CliRunner
from pytest import ExitCode

from awattar import cli


def test_get_version() -> None:
    runner = CliRunner()
    result = runner.invoke(cli.version)
    assert result.exit_code == ExitCode.OK
    assert "Version: " in result.output


def test_get_cliprompt() -> None:
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == ExitCode.OK

    cli_prompt_message = result.output.splitlines()

    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in cli_prompt_message[0]
