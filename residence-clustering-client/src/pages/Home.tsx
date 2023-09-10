import { Stack, Typography } from "@mui/material";
import Button from "@mui/material/Button";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import TextField from "@mui/material/TextField";
import { FormEventHandler, useState } from "react";
import { useMutation } from "react-query";
import Loading from "../components/Loading";
import { api } from "../services/api";
import { LocationSelect } from "../types";

export default function Home() {
  // state ---------------------------------------------------------------------

  const [locationSearch, setLocationSearch] = useState("");
  const [locationSelect, setLocationSelect] = useState<string>("");
  const [latLon, setLatLon] = useState<{
    latitude: string;
    longitude: string;
  }>({ latitude: "", longitude: "" });

  // query and mutation --------------------------------------------------------

  const locationSearchMutation = useMutation((locationSearchQuery: string) =>
    api.locationSearch(locationSearchQuery)
  );

  const locationSelectMutation = useMutation((locSelectData: LocationSelect) =>
    api.locationSelect(locSelectData)
  );

  // functions -----------------------------------------------------------------

  const handleSelectChange = (event: SelectChangeEvent) => {
    setLocationSelect(event.target.value);
  };

  const handleSubmit: FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
    if (locationSearch.trim().length > 0) {
      locationSearchMutation.mutate(locationSearch);
    }
  };

  // jsx -----------------------------------------------------------------------

  return (
    <Stack spacing={2} useFlexGap>
      <Typography variant="h4" component={"h1"} paddingTop={1}>
        Clustering of Residential Buildings Based on Proximity to Amenities
      </Typography>
      <Stack
        direction={"row"}
        spacing={1}
        useFlexGap
        component={"form"}
        onSubmit={handleSubmit}
      >
        <TextField
          value={locationSearch}
          onChange={(e) => setLocationSearch(e.target.value)}
          id="outlined-basic"
          size="small"
          label="Location"
          variant="outlined"
        />
        <Button size="small" variant="contained" disableElevation type="submit">
          Search
        </Button>
      </Stack>
      {locationSearchMutation.isLoading ? (
        <Loading />
      ) : (
        <>
          {locationSearchMutation.isError ? (
            <div>
              An error occurred: {(locationSearchMutation.error as any).message}
            </div>
          ) : null}

          {locationSearchMutation.isSuccess ? (
            <Stack spacing={2} useFlexGap>
              <Typography>
                Select one of the{" "}
                {locationSearchMutation.data.data.results.length} matches found:
              </Typography>
              <FormControl sx={{ m: 1, width: 500 }} size="small">
                <InputLabel id="demo-select-small-label">
                  Select location
                </InputLabel>
                <Select
                  labelId="demo-select-small-label"
                  id="demo-select-small"
                  value={locationSelect}
                  label="Select location"
                  onChange={handleSelectChange}
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>

                  {locationSearchMutation.data.data.results.map((loc) => {
                    const value = `${loc.text.primary}, ${loc.text.secondary}`;
                    return (
                      <MenuItem key={value} value={value}>
                        {value}
                      </MenuItem>
                    );
                  })}
                </Select>
              </FormControl>
              <Stack spacing={1} useFlexGap>
                <Typography>Or enter Latitude and Longitude</Typography>
                <Stack direction={"row"} spacing={1} useFlexGap>
                  <TextField
                    value={latLon.latitude}
                    onChange={(e) =>
                      setLatLon({ ...latLon, latitude: e.target.value })
                    }
                    size="small"
                    label="Latitude"
                    variant="outlined"
                  />
                  <TextField
                    value={latLon.longitude}
                    onChange={(e) =>
                      setLatLon({ ...latLon, longitude: e.target.value })
                    }
                    size="small"
                    label="Longitude"
                    variant="outlined"
                  />
                </Stack>
              </Stack>
              <Button
                size="small"
                sx={{
                  width: 30,
                }}
                variant="contained"
                disableElevation
                type="button"
                onClick={() => {
                  // if location is selected
                  if (locationSelect) {
                    const data = locationSearchMutation.data.data.results.find(
                      (l) =>
                        `${l.text.primary}, ${l.text.secondary}` ===
                        locationSelect
                    );
                    if (data) {
                      locationSelectMutation.mutate({
                        primary: data.text.primary,
                        secondary: data.text.secondary,
                        type: data.type,
                        address_id: data.address?.address_id,
                        latitude: data.place?.geocodes.main.latitude,
                        longitude: data.place?.geocodes.main.longitude,
                      });
                    }
                  } else {
                    // if latitude, longitude is provided
                    locationSelectMutation.mutate({
                      latitude: parseFloat(latLon.latitude),
                      longitude: parseFloat(latLon.longitude),
                    });
                  }
                }}
              >
                Submit
              </Button>
            </Stack>
          ) : null}
        </>
      )}
      {locationSelectMutation.isLoading ? (
        <Loading />
      ) : (
        <Stack useFlexGap>
          {locationSelectMutation.isError ? (
            <div>
              An error occurred: {(locationSelectMutation.error as any).message}
            </div>
          ) : null}

          {locationSelectMutation.isSuccess ? (
            <>
              {locationSelectMutation.data?.data.error ? (
                <div>{locationSelectMutation.data?.data.error}</div>
              ) : (
                <iframe srcDoc={locationSelectMutation.data?.data}></iframe>
              )}
            </>
          ) : null}
        </Stack>
      )}
    </Stack>
  );
}
