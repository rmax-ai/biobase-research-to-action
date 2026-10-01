"""Bootstrap smoke test: the package imports and reports a version."""

import research_to_action


def test_package_imports() -> None:
    assert research_to_action.__version__ == "0.1.0"
