#!/usr/bin/env python3
"""(DEPRECATED) build_alias_index

Alias infrastructure has been removed from this repository.

FrameURL is the only normative identifier.

This legacy tool intentionally fails if invoked.
"""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "ERROR: alias infrastructure has been removed; FrameURL is the only identifier.\n"
        "ERROR: tools/build_alias_index is deprecated and should not be invoked.",
        file=sys.stderr,
    )
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
