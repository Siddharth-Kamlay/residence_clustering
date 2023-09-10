import axios from "axios";
import { LocationSearchResponse, LocationSelect } from "../types";
console.log(import.meta.env.VITE_API_BASE_URL);
const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const api = {
  locationSearch: (query: string) => {
    return API.post<LocationSearchResponse>("locations", {
      query,
    });
  },
  locationSelect: (data: LocationSelect) => {
    return API.post("locationSelect", data);
  },
};
