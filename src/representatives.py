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

import json
from typing import Optional, Union

from src.config import BASE_DIR
from src.exceptions import NotFoundError, ValidationError

CURRENT_LEGISLATORS = json.loads((BASE_DIR / "legislators-current.json").read_text())


def get_federal_representatives(
    state: str,
    district: Optional[Union[int, str]] = None,
    *,
    all_house: bool = False,
    all_house_regardless: bool = False,
) -> list[dict]:
    """
    Gets federal level Senators and House of Representatives.

    :param state: Two letter code for your state. Non-voting districts
    also have one like American Samoa, AS.
    :param district: optional district number. It could also be AL for at large
    due to single member states.
    :param all_house: if you only specify a state and no district, then all HR
    for the state will be returned
    :param all_house_regardless: regardless if a district is specified,
    all HR for the state will be returned
    """
    try:
        assert len(state) == 2
        state_data: dict = CURRENT_LEGISLATORS[state]
    except AssertionError:
        raise ValidationError("You must specify a state using its two letter code")
    except KeyError:
        raise NotFoundError("State not found")
    data: list = state_data.get("senators", [])
    if all_house_regardless:
        return data + [v for k, v in state_data.items() if k != "senators"]
    if district:
        # Convert district first
        if len(district) > 3:
            # Prevents "senators" key to be chosen
            raise ValidationError("Districts can only be 2 digit integers")
        try:
            data.append(state_data[str(district)])
        except (TypeError, KeyError):
            # Allow pass; even though district DNE, we still got some data anyways
            pass
    elif all_house:
        return data + [v for k, v in state_data.items() if k != "senators"]
    return data
