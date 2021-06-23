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

import os
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from geopandas import read_file
from shapely.geometry import Point
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


if TYPE_CHECKING:
    from starlette.requests import Request

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# Only 16-25kb of memory
GEOJSON = read_file(BASE_DIR / "districts.geojson")


def get_district(index: int) -> str:
    # Possible to have TypeError if non-voting district
    # since their GeoJSON isn't valid?
    return GEOJSON.values[index][0][0]


async def find_district(request: "Request"):
    # noinspection PyBroadException
    try:
        data: dict = await request.json()
        point = Point(float(data["longitude"]), float(data["latitude"]))
        index = np.where(GEOJSON.contains(point))[0]
        return JSONResponse({"district": get_district(index)})
    except IndexError:
        return JSONResponse({"error": "could not find district"}, status_code=400)
    except TypeError:
        return JSONResponse(
            {
                "error": "you live in a non voting district. We're working on fixing that as soon as possible"
            },
            status_code=400,
        )
    except Exception:
        return JSONResponse({"error": "could not parse json"}, status_code=400)


app = Starlette(
    debug=os.environ.get("DEBUG", False),
    routes=[Route("/find-district", find_district)],
)
