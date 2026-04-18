"""Tests to verify all modules can be imported and that __init__.py is consistent."""

import ast
import importlib
from pathlib import Path

import pytest

PACKAGE_DIR = Path(__file__).resolve().parent.parent / "ruf_common"

# Internal sub-modules that are not part of the public API
# (imported by other modules, not re-exported from __init__.py)
_INTERNAL_MODULES = {"database_sqlite3"}


def _get_module_files():
    """Return the set of module names derived from .py files in the package directory."""
    return {
        p.stem
        for p in PACKAGE_DIR.glob("*.py")
        if p.stem != "__init__" and not p.name.startswith("_")
    }


def _get_public_module_files():
    """Return module files excluding known internal sub-modules."""
    return _get_module_files() - _INTERNAL_MODULES


def _parse_init():
    """Parse __init__.py and return the set of imported names and the __all__ list."""
    init_path = PACKAGE_DIR / "__init__.py"
    source = init_path.read_text()
    tree = ast.parse(source, filename=str(init_path))

    imports = set()
    all_list = None

    for node in ast.walk(tree):
        # Catch `from . import foo`
        if isinstance(node, ast.ImportFrom) and node.module is None and node.level == 1:
            for alias in node.names:
                imports.add(alias.name)
        # Catch `__all__ = [...]`
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, ast.List):
                        all_list = {
                            elt.value
                            for elt in node.value.elts
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                        }

    return imports, all_list


# ---------------------------------------------------------------------------
# Consistency tests — these would have caught the aws issue
# ---------------------------------------------------------------------------

class TestPackageConsistency:
    """Verify __init__.py imports, __all__, and module files are all in sync."""

    def test_no_imports_without_module_files(self):
        """Every 'from . import X' in __init__.py must have a corresponding .py file."""
        imports, _ = _parse_init()
        module_files = _get_module_files()
        missing_files = imports - module_files
        assert not missing_files, (
            f"__init__.py imports modules that have no .py file: {sorted(missing_files)}"
        )

    def test_no_all_entries_without_module_files(self):
        """Every entry in __all__ must have a corresponding .py file."""
        _, all_list = _parse_init()
        assert all_list is not None, "__all__ is not defined in __init__.py"
        module_files = _get_module_files()
        missing_files = all_list - module_files
        assert not missing_files, (
            f"__all__ lists modules that have no .py file: {sorted(missing_files)}"
        )

    def test_no_all_entries_without_import(self):
        """Every entry in __all__ must have a matching 'from . import' statement."""
        imports, all_list = _parse_init()
        assert all_list is not None, "__all__ is not defined in __init__.py"
        missing_imports = all_list - imports
        assert not missing_imports, (
            f"__all__ lists modules not imported in __init__.py: {sorted(missing_imports)}"
        )

    def test_no_imports_missing_from_all(self):
        """Every 'from . import X' should be listed in __all__."""
        imports, all_list = _parse_init()
        assert all_list is not None, "__all__ is not defined in __init__.py"
        missing_from_all = imports - all_list
        assert not missing_from_all, (
            f"__init__.py imports modules not listed in __all__: {sorted(missing_from_all)}"
        )

    def test_no_public_module_files_missing_from_init(self):
        """Every public .py module file should be imported in __init__.py."""
        imports, _ = _parse_init()
        public_modules = _get_public_module_files()
        not_imported = public_modules - imports
        assert not not_imported, (
            f"Module files exist but are not imported in __init__.py: {sorted(not_imported)}"
        )


# ---------------------------------------------------------------------------
# Import tests — verify each module actually loads at runtime
# ---------------------------------------------------------------------------

class TestModuleImports:
    """Verify all modules in the ruf_common package can be imported."""

    def test_import_ruf_common(self):
        """Test importing the main package."""
        import ruf_common
        assert ruf_common is not None

    @pytest.mark.parametrize("module_name", sorted(_get_public_module_files()))
    def test_import_module(self, module_name):
        """Test that each module file can be imported from the package."""
        mod = importlib.import_module(f"ruf_common.{module_name}")
        assert mod is not None

    def test_all_entries_importable(self):
        """Every entry in __all__ must be importable."""
        _, all_list = _parse_init()
        assert all_list is not None
        for name in sorted(all_list):
            mod = importlib.import_module(f"ruf_common.{name}")
            assert mod is not None, f"Could not import ruf_common.{name}"
