import json
import os
from dataclasses import dataclass, field
from typing import Dict

from decouple import config


@dataclass(frozen=True)
class Configs:
    token: str = field(init=False, repr=False, default=config("TOKEN"))
    command_prefix: str
    case_insensitive: bool
    soundfx_directory: str
    soundfx: Dict[str, str]


def _get_configs():
    abs_path = os.path.abspath(os.path.dirname(__file__))
    raw_json = {}
    with open(f"{abs_path}/../../config.json") as configs:
        raw_json = json.load(configs)
    return Configs(**raw_json)


CONFIGS = _get_configs()


if __name__ == "__main__":
    print(CONFIGS)
