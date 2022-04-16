from logging import Logger

import mock
from fastapi_mvc.generators import Generator


@mock.patch.multiple(
    "fastapi_mvc.generators.base.Generator",
    __abstractmethods__=set()
)
def test_base_generator():
    assert not hasattr(Generator, "name")
    assert not hasattr(Generator, "template")
    assert not hasattr(Generator, "usage")
    assert Generator.cli_arguments == [
        {
            "param_decls": ["NAME"],
            "required": True,
            "nargs": 1,
        }
    ]
    assert Generator.cli_options == [
        {
            "param_decls": ["-S", "--skip"],
            "is_flag": True,
            "help": "Skip files that already exist.",
        }
    ]

    parser = mock.Mock()
    parser.package_name = "test_app"
    parser.folder_name = "test-app"

    generator = Generator(
        parser=parser,
        project_root="/some/path"
    )

    generator.new()
    generator.destroy()

    assert isinstance(generator, Generator)
    assert not hasattr(generator, "__dict__")
    assert hasattr(generator, "__slots__")
    assert generator.__slots__ == (
        "_log",
        "_parser",
        "_project_root",
        "_context",
    )

    assert isinstance(generator._log, Logger)
    assert generator._parser == parser
    assert generator._project_root == "/some/path"
    assert generator._context == {
        "package_name": "test_app",
        "folder_name": "test-app",
    }