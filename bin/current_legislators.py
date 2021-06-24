# Copyright 2021 Andrew Chen Wang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime as dt
import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Optional, Tuple, Union

import requests


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


def find_state_and_district(
    terms: list,
    *,
    stringify_district: bool = False,
) -> tuple[str, Optional[Union[str, int]]]:
    """
    Gets state and district where representative is from
    :param terms: a list of the terms with a key "end" in date form e.g. 2021-01-06
    :param stringify_district: whether to convert district to a string or keep as int
    :return: tuple of state and district
    """
    term = sorted(terms, key=lambda x: dt.datetime.strptime(x["end"], "%Y-%m-%d"))[-1]
    district = term.get("district")
    return term["state"], str(district) if stringify_district else district


def order_file(original_data: list) -> dict:
    """
    Using the https://github.com/unitedstates/congress-legislators
    legislators-current.json dataset, we re-order it into a friendlier
    file for lookup via state and district.
    """
    data = dict()
    for x in original_data:
        state, district = find_state_and_district(x["terms"])
        _copied = deepcopy(x)
        if district:
            data.setdefault(state, {district: _copied}).setdefault(district, _copied)
        else:
            data.setdefault(state, {"senators": []}).setdefault("senators", []).append(
                _copied
            )
    return data


def run(url="https://theunitedstates.io/congress-legislators/legislators-current.json"):
    data: list = requests.get(url).json()
    # Put it in an optimized order
    with (BASE_DIR / "legislators-current.json").open("w") as f:
        json.dump(order_file(data), f, indent=0 if os.environ.get("CI") else 2)


if __name__ == "__main__":
    run()
