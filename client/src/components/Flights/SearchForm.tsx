import React from "react";
import { Button, TextField, CircularProgress } from "@mui/material";
import Autocomplete from "@mui/material/Autocomplete";

interface SearchFormProps {
  fromCity: string;
  toCity: string;
  date: string;
  dateBack: string;
  adults: number;
  fromCityOptions: string[];
  toCityOptions: string[];
  loading: boolean;
  onFromCityChange: (city: string) => void;
  onToCityChange: (city: string) => void;
  onDateChange: (date: string) => void;
  onDateBackChange: (date: string) => void;
  onAdultsChange: (adults: number) => void;
  onSearch: () => void;
}

const SearchForm: React.FC<SearchFormProps> = ({
  fromCity,
  toCity,
  date,
  fromCityOptions,
  toCityOptions,
  loading,
  dateBack,
  adults,
  onFromCityChange,
  onToCityChange,
  onDateChange,
  onDateBackChange,
  onAdultsChange,
  onSearch,
}) => (
  <div className="flex justify-center items-center h-1/2 bg-primary">
    <div className="flex flex-wrap space-x-2 bg-white/30 p-4 rounded-lg shadow-lg my-10 ">
      <div className="flex-1 w-40 mt-4 md:mt-0">
        <Autocomplete
          className="w-full"
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
      </div>
      <div className="flex-1 w-40 mt-4 md:mt-0">
        <Autocomplete
          className="w-full"
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
      </div>
      <div className="flex-1 w-40 mt-4 md:mt-0">
        <TextField
          className="w-full"
          label="Date from"
          type="date"
          value={date}
          onChange={(event) => onDateChange(event.target.value)}
          InputLabelProps={{
            shrink: true,
          }}
        />
      </div>
      <div className="flex-1 w-40 mt-4 md:mt-0">
        <TextField
          className="w-full"
          label="Date to"
          type="date"
          value={dateBack}
          onChange={(event) => onDateBackChange(event.target.value)}
          InputLabelProps={{
            shrink: true,
          }}
        />
      </div>
      <div className="flex-1 w-40 mt-4 md:mt-0">
        <TextField
          className="w-full"
          label="Adults"
          type="number"
          value={adults}
          onChange={(event) => onAdultsChange(Number(event.target.value))}
          InputLabelProps={{
            shrink: true,
          }}
        />
      </div>
      <div className="flex items-end mt-4 md:mt-0">
        <Button
          variant="contained"
          onClick={onSearch}
          disabled={loading}
          className="flex justify-center items-center px-4 py-2 rounded-md w-full md:w-auto bg-danger text-secondary"
        >
          {loading ? (
            <CircularProgress size={30} color="secondary" />
          ) : (
            "Search"
          )}
        </Button>
      </div>
    </div>
  </div>
);

export default SearchForm;
