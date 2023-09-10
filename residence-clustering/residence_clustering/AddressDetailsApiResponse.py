from typing import TypedDict


class LatitudeLongitude(TypedDict):
    latitude: float
    longitude: float


class Geocodes(TypedDict):
    drop_off: LatitudeLongitude
    front_door: LatitudeLongitude
    main: LatitudeLongitude
    road: LatitudeLongitude
    roof: LatitudeLongitude


class AddressDetailsApiResponse(TypedDict):
    geocodes: Geocodes
