import sys
import os
import importlib.util
import pkgutil

from fastapi_mvc.generators import Generator


PROJECT_ROOT = os.getcwd()


def load_generators():
    """
    https://docs.python.org/3/library/importlib.html#importing-programmatically

    Returns:

    """
    generators = dict()

    builtins = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../code",
        )
    )
    local = os.path.abspath(
        os.path.join(
            PROJECT_ROOT,
            "lib/generators",
        )
    )

    for item in pkgutil.iter_modules([builtins, local]):
        m_path = os.path.join(
            item.module_finder.path,
            item.name,
            "__init__.py",
        )
        spec = importlib.util.spec_from_file_location(
            "fastapi_mvc_generators",
            m_path,
        )
        module = importlib.util.module_from_spec(spec)
        # Register module before running `exec_module()` to make all submodules
        # in it able to find their parent package (i.e. `fastapi_mvc_generators`).
        # Otherwise, we will got the following error:
        #     `ModuleNotFoundError: No module named 'fastapi_mvc_generators'`
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        generator = getattr(module, "__all__")

        if issubclass(generator, Generator):
            generators[generator.name] = generator

    return generators
