"""Bootstrap smoke test: the package imports and reports a version."""

import governed_clinical_actions


def test_package_imports() -> None:
    assert governed_clinical_actions.__version__ == "0.1.0"
