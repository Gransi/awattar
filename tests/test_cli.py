import json
import logging

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


""" def test_get_fetch_prices_day(capsys) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.fetch_prices, catch_exceptions=True)
    assert result.exit_code == ExitCode.OK

    out, err = capsys.readouterr()

    print(result.stderr)
    print("results:")
    print(result.stdout)
    json_object = json.loads(result.stdout)

    logging.info(len(json_object))

    assert len(json_object) == 2 """
