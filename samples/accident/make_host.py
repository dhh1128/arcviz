#!/usr/bin/env python3
"""Regenerate host.json's aliases with the COIA reference implementation.

The host's alias lookup is fictional, but the aliases it returns should be real COIA aliases,
so they are minted here by the spec's own oracle (~/code/me/coia/coia.py, `create_alias`) from
who/role/scope answers, rather than typed by hand. The answers are kept in host.json beside the
result so a reader can see what each alias was made from. arcviz itself never mints an alias;
this script plays the host.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / "code" / "me" / "coia"))
import coia  # noqa: E402  the spec's oracle, not an arcviz module

# AID -> (who, role, scope). Invented for this sample.
ANSWERS = {
    "EL37ZkrKxqN-2hkOCDDaaeb7ozbmM6BTYpczUEBqQm74": ("Rosa Iqbal", "claims adjuster", "Northgate Mutual"),
    "EPVcVcU46oTcO1b_9GPi35bHlyiLz8Zqv0s9ziEjhTB-": ("Utah DLD", "licensing authority", ""),
    "EDENM0x7P_uvLaT4RFlYxouW4tj37ZELUJtN7uYiN_UP": ("Alice Moreau", "driver", ""),
    "EKkmidwYBfZLXEstkVnvHJeE-bnoeQcGzoF29AJ6ViyC": ("Jae Park", "witness", ""),
    "EDV3OZ37h8Z8Ii5qi-YeHy6lDP04geVaZF_-zUdEFNGw": ("Northgate Mutual", "claims intake", ""),
    "ELTGvn2ZmepBNl0JkXyPfjnd_DEYvXHxK-AiUMBoKr40": ("GLEIF", "root of trust", "vLEI"),
    "EOvbsyiKJgxQxsQVfIsZTch5ay6NvcEh0T7GFoy3b48S": ("Fixture QVI", "qualified issuer", "vLEI"),
    "EErZ90n2jH2yBA4CjlZ03jzJx17wR653gpqUspe1p_RZ": ("Fixture Corp", "legal entity", "vLEI"),
}


def main() -> int:
    path = HERE / "host.json"
    host = json.loads(path.read_text())
    host["aliases"] = {aid: coia.create_alias("en", *a) for aid, a in ANSWERS.items()}
    host["alias_answers"] = {aid: {"who": w, "role": r, "scope": s} for aid, (w, r, s) in ANSWERS.items()}
    path.write_text(json.dumps(host, indent=1, ensure_ascii=False) + "\n")
    for aid, alias in host["aliases"].items():
        print(aid[:10], alias)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
