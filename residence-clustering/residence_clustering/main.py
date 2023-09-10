from typing import List, Tuple
import pandas as pd
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from .AutocompleteApiResponse import AutocompleteApiResponse
from .PlaceSearchApiResponse import PlaceSearchApiResponse
from .PlaceSearchCategory import PlaceSearchCategory
from .AddressDetailsApiResponse import AddressDetailsApiResponse
from fastapi import FastAPI
from enum import Enum
from dataclasses import dataclass
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import folium
from folium import plugins

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "accept": "application/json",
    "Authorization": "fsq3I0WkNOJPlcmZ17tbS3WN06fCNt3VgH9Lht2z1Tl/hu4=",
}


def fetch_get(url: str):
    response = requests.get(url, headers=HEADERS)
    return response.json()


def search_location(query: str) -> AutocompleteApiResponse:
    URL = f"https://api.foursquare.com/v3/autocomplete?query={query}&radius=10000&limit=10"
    return fetch_get(URL)


def address_details(id: str) -> AddressDetailsApiResponse:
    URL = f"https://api.foursquare.com/v3/address/{id}"
    return fetch_get(URL)


def place_search(
    lat_lon: Tuple[float, float], categories: List[PlaceSearchCategory]
) -> PlaceSearchApiResponse:
    print(categories)
    URL = f"https://api.foursquare.com/v3/places/search?ll={lat_lon[0]}%2C{lat_lon[1]}&radius=10000&categories={'%2C'.join(map(str, categories))}&limit=30"
    print(URL)
    return fetch_get(URL)


@app.get("/")
def read_root():
    return {"Hello": "World"}


class LocationSearch(BaseModel):
    query: str


@app.post("/locations")
def getLocations(body: LocationSearch):
    locations = search_location(body.query)
    return locations


class LocationSelect(BaseModel):
    type: str | None = None
    address_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    primary: str | None = None
    secondary: str | None = None


@app.post("/locationSelect")
def selectLocation(body: LocationSelect):
    l = []
    n = []

    if body.type is None:
        # only lat, lon are provided
        l.append(body.longitude)
        l.append(body.latitude)
        n.append(l[0])
        n.append(l[1])
    else:
        if body.type == "address":
            print(body.address_id, body.primary)
            add = body.address_id
            n.append(body.primary)

            j2: AddressDetailsApiResponse = address_details(add)

            l.append(j2["geocodes"]["main"]["latitude"])
            l.append(j2["geocodes"]["main"]["longitude"])

        elif body.type == "place":
            l.append(body.latitude)
            l.append(body.longitude)
            n.append(body.primary)

    j3 = place_search((l[0], l[1]), [PlaceSearchCategory["ResidentialBuilding"]])
    print("---------------------try j3-----------------------")
    print(j3)
    print("---------------------try j3-----------------------")

    if len(j3["results"]) == 0:
        return {"error": "No registered residental buildings present"}

    else:
        df = pd.DataFrame(j3["results"])

        lon = []
        lat = []
        name = []

        for res in j3["results"]:
            lat.append(res["geocodes"]["main"]["latitude"])
            lon.append(res["geocodes"]["main"]["longitude"])
            name.append(res["name"])

        f2 = pd.DataFrame.from_dict({"Lat": lat, "Lng": lon, "Name": name})

        l2 = []

        for i in range(len(lat)):
            j4 = place_search(
                (lat[i], lon[i]),
                [
                    PlaceSearchCategory["FruitAndVegetableStore"],
                    PlaceSearchCategory["GroceryStore"],
                    PlaceSearchCategory["OrganicGrocery"],
                ],
            )
            K = len(j4["results"])
            l2.append(K)

        l3 = []

        for i in range(len(lat)):
            j4 = place_search((lat[i], lon[i]), [PlaceSearchCategory["GymAndStudio"]])
            K = len(j4["results"])
            l3.append(K)

        l4 = []

        for i in range(len(lat)):
            j4 = place_search((lat[i], lon[i]), [PlaceSearchCategory["Restaurant"]])
            K = len(j4["results"])
            l4.append(K)

        fi_data = {
            "Lat": lat,
            "Lng": lon,
            "Fruits_Vegetables": l2,
            "Res": l4,
            "Sports": l3,
        }

        final_df = pd.DataFrame.from_dict(fi_data)

        x = final_df.iloc[:, [0, 1, 2, 3, 4]].values

        mean = KMeans(n_clusters=3)
        y = mean.fit_predict(x)

        final_df["Cluster"] = y

        # figure, axis = plt.subplots(1, 3, figsize=(15, 5))
        # for i in range(3):
        #     plt.sca(axis[i])
        #     sns.boxplot(
        #         data=final_df[final_df["Cluster"] == i].drop(
        #             ["Lat", "Lng", "Cluster"], axis=1
        #         )
        #     )
        #     plt.xticks(rotation=45)
        #     if i == 0:
        #         plt.title("Green")
        #     elif i == 1:
        #         plt.title("Yellow")
        #     else:
        #         plt.title("Red")

        # plt.show()

        map_bom = folium.Map(location=l, zoom_start=12)
        locations = folium.map.FeatureGroup()

        def color_producer(cluster):
            if cluster == 0:
                return "green"
            elif cluster == 1:
                return "orange"
            else:
                return "red"

        latitudes = list(final_df["Lat"])
        longitudes = list(final_df["Lng"])
        labels = list(final_df["Cluster"])
        names = list(f2["Name"])
        for lat, lng, labels, names in zip(latitudes, longitudes, labels, names):
            folium.CircleMarker(
                [lat, lng],
                fill=True,
                fill_opacity=1,
                popup=folium.Popup(names, max_width=300),
                radius=10,
                color=color_producer(labels),
            ).add_to(map_bom)

        map_bom.add_child(locations)
        folium.Marker(l, popup=n[0]).add_to(map_bom)

        return map_bom.get_root().render()

    # %%


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
