export interface LocationSearch {
  type: "address" | "place";
  text: {
    primary: string;
    secondary: string;
  };
  address?: {
    address_id: string;
  };
  place?: {
    geocodes: {
      main: {
        latitude: number;
        longitude: number;
      };
    };
  };
}

export interface LocationSearchResponse {
  results: LocationSearch[];
}

export interface LocationSelect {
  type?: string;
  address_id?: string;
  latitude?: number;
  longitude?: number;
  primary?: string;
  secondary?: string;
}
