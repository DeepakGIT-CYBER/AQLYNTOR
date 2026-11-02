"""Deprecated project generator.

This legacy script is intentionally disabled. Its previous implementation
rewrote current project files with outdated, unsafe templates. Use the
documented project setup and migration instructions instead.
"""


def build_project() -> None:
    raise RuntimeError(
        "The legacy generator is disabled because it overwrites current "
        "AQLYNTOR modules with outdated templates."
    )


if __name__ == "__main__":
    raise SystemExit(
        "AQLYNTOR: core/setup_full.py is deprecated and cannot be executed."
    )
