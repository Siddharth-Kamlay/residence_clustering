from typing import TypedDict
from datetime import datetime
from typing import List


class Icon(TypedDict):
    prefix: str
    suffix: str


class Category(TypedDict):
    id: int
    name: str
    icon: Icon


class LatitudeLongitude(TypedDict):
    latitude: float
    longitude: float


class Geocodes(TypedDict):
    drop_off: LatitudeLongitude
    main: LatitudeLongitude
    roof: LatitudeLongitude


class Location(TypedDict):
    country: str
    formatted_address: str
    locality: str
    postcode: str
    region: str


class Place(TypedDict):
    fsq_id: str
    categories: List[Category]
    distance: int
    geocodes: Geocodes
    location: Location
    name: str


class Highlight(TypedDict):
    start: int
    length: int


class Text(TypedDict):
    primary: str
    secondary: str
    highlight: List[Highlight]


class Tip(TypedDict):
    id: str
    created_at: datetime
    text: str
    url: str
    photo: str
    lang: str
    agree_count: int
    disagree_count: int


class AutocompleteResultIcon(TypedDict):
    id: str
    created_at: datetime
    prefix: str
    suffix: str
    width: int
    height: int
    classifications: List[str]
    tip: Tip


class Address(TypedDict):
    address_id: str


class SearchCategoryIconTip(TypedDict):
    id: str
    created_at: datetime
    text: str
    url: str
    photo: str
    lang: str
    agree_count: int
    disagree_count: int


class SearchCategoryIcon(TypedDict):
    id: str
    created_at: datetime
    prefix: str
    suffix: str
    width: int
    height: int
    classifications: List[str]
    tip: SearchCategoryIconTip


class SearchCategory(TypedDict):
    id: int
    name: str
    icon: SearchCategoryIcon


class SearchChain(TypedDict):
    id: str
    name: str


class Search(TypedDict):
    query: str
    category: SearchCategory
    chain: SearchChain


class GeoCenter(LatitudeLongitude):
    pass


class GeoBoundsNe(LatitudeLongitude):
    pass


class GeoBoundsSw(LatitudeLongitude):
    pass


class GeoBounds(TypedDict):
    ne: GeoBoundsNe
    sw: GeoBoundsSw


class Geo(TypedDict):
    name: str
    center: GeoCenter
    bounds: GeoBounds
    cc: str
    type: str


class Debug(TypedDict):
    score: int


class Result(TypedDict):
    type: str
    text: Text
    icon: AutocompleteResultIcon
    link: str
    place: Place
    address: Address
    search: Search
    geo: Geo
    debug: Debug


class AutocompleteApiResponse(TypedDict):
    results: List[Result]
