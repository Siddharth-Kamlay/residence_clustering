from typing import TypedDict, List
from .AddressDetailsApiResponse import Geocodes


class Result(TypedDict):
    geocodes: Geocodes
    name: str


class PlaceSearchApiResponse(TypedDict):
    results: List[Result]
