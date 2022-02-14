import mock
import pytest
from fastapi_mvc.cli.commands.run import run


def test_run_help(cli_runner):
    result = cli_runner.invoke(run, ["--help"])
    assert result.exit_code == 0


def test_run_invalid_options(cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.run.Context")
def test_run_default_values(context_mock, cli_runner):
    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0

    context_mock.return_value.execute.assert_called_once_with(
        host="127.0.0.1", port="8000"
    )


@pytest.mark.parametrize(
    "options, expected",
    [
        (
            ["--host", "10.20.30.40", "--port", "1234"],
            {"host": "10.20.30.40", "port": "1234"}
        ),
        (
            ["--host", "192.168.0.10", "-p", "9001"],
            {"host": "192.168.0.10", "port": "9001"}
        )
    ]
)
@mock.patch("fastapi_mvc.cli.commands.run.Context")
def test_run_with_options(context_mock, cli_runner, options, expected):
    result = cli_runner.invoke(run, options)
    assert result.exit_code == 0

    context_mock.return_value.execute.assert_called_once_with(**expected)
