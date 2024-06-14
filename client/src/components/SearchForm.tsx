import React from "react";
import { Button, TextField, CircularProgress } from "@mui/material";
import Autocomplete from "@mui/material/Autocomplete";

interface SearchFormProps {
  fromCity: string;
  toCity: string;
  date: string;
  fromCityOptions: string[];
  toCityOptions: string[];
  loading: boolean;
  onFromCityChange: (city: string) => void;
  onToCityChange: (city: string) => void;
  onDateChange: (date: string) => void;
  onSearch: () => void;
}

const SearchForm: React.FC<SearchFormProps> = ({
  fromCity,
  toCity,
  date,
  fromCityOptions,
  toCityOptions,
  loading,
  onFromCityChange,
  onToCityChange,
  onDateChange,
  onSearch,
}) => (
  <div className="flex justify-between items-center border border-gray-300 rounded-lg p-14">
    <Autocomplete
      className="w-1/4 p-4"
      freeSolo
      value={fromCity}
      onChange={(_, newValue) => onFromCityChange(newValue || "")}
      options={fromCityOptions}
      renderInput={(params) => (
        <TextField
          {...params}
          label="From"
          variant="outlined"
          onChange={(event) => onFromCityChange(event.target.value)}
        />
      )}
    />
    <Autocomplete
      className="w-1/4 p-4"
      freeSolo
      value={toCity}
      onChange={(_, newValue) => onToCityChange(newValue || "")}
      options={toCityOptions}
      renderInput={(params) => (
        <TextField
          {...params}
          label="To"
          variant="outlined"
          onChange={(event) => onToCityChange(event.target.value)}
        />
      )}
    />
    <TextField
      className="w-1/4 p-4"
      label="Date from"
      type="date"
      value={date}
      onChange={(event) => onDateChange(event.target.value)}
      InputLabelProps={{
        shrink: true,
      }}
    />
    <Button
      className="size-20 p-4 rounded"
      variant="contained"
      onClick={onSearch}
      disabled={loading}
    >
      {loading ? <CircularProgress size={30} /> : "Search"}
    </Button>
  </div>
);

export default SearchForm;
