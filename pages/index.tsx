import { Inter } from "next/font/google";
import * as React from "react";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import { useState } from "react";
import Stack from "@mui/material/Stack";
import Image from "next/image";
import CircularProgress from "./components";

const inter = Inter({ subsets: ["latin-ext"] });

const inputStyle = {
  color: "white",
};

const companyTickers = [
  { name: "Apple", ticker: "AAPL" },
  { name: "Goldman Sachs", ticker: "GS" },
  { name: "Microsoft", ticker: "MSFT" },
];

export default function Home() {
  // pull in the company tickers from the database
  const [companyTickers, setCompanyTickers] = useState(
    [{ name: "Apple", ticker: "AAPL" },
    { name: "Goldman Sachs", ticker: "GS" },
    { name: "Microsoft", ticker: "MSFT" },]
  );
  const [selectedTicker, setSelectedTicker] = useState("AAPL");
  const [selectedCompetitorTickers, setSelectedCompetitorTickers] = useState([
    "MSFT",
  ]);

  React.useEffect(() => {
    fetch("http://127.0.0.1:5000/companies")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setCompanyTickers(data);
      });
  }, []);

  const handleButtonClick = () => {
    console.log(selectedTicker);
    fetch("http://127.0.0.1:5000/predict/" + selectedTicker);
  };

  return (
    <>
      <div className="px-4 py-4">
        <img src="logo.svg" alt=""></img>
      </div>
      <div className="flex justify-center gap-x-20 py-16">
        <Autocomplete
          disablePortal
          id="combo-box-demo"
          options={companyTickers}
          defaultValue={companyTickers[0]}
          sx={{ width: 300 }}
          getOptionLabel={(option) => option.ticker}
          renderInput={(params) => {
            const selectedOption = companyTickers.find(
              (option) => option.ticker === selectedTicker
            );
            return (
              <div style={{ display: "flex", alignItems: "center" }}>
                <TextField
                  {...params}
                  label="Company Ticker"
                  variant="outlined"
                  value={selectedOption ? selectedOption.ticker : ""}
                  style={{ flex: 1 }} // Expand to fill the remaining space
                />
                <Image
                  src={`/Logos/${selectedOption.ticker}.png`}
                  alt={selectedOption.ticker}
                  width="20"
                  height="20"
                  style={{ marginLeft: "8px" }} // Adjust the margin as needed
                />
              </div>
            );
          }}
          getOptionSelected={(option, value) => option.ticker === value.ticker}
          renderOption={(props, option) => (
            <li {...props}>
              <Image
                src={`/Logos/${option.ticker}.png`}
                alt={option.ticker}
                width="20"
                height="20"
                style={{ marginRight: "8px" }} // Adjust the margin as needed
              />
              {option.ticker}
            </li>
          )}
        />

        <Stack spacing={3} sx={{ width: 500 }}>
          <Autocomplete
            multiple
            id="tags-standard"
            options={companyTickers}
            getOptionLabel={(option) => option.ticker}
            defaultValue={[companyTickers[0]]}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="standard"
                label="Competitor Companies"
                placeholder="Add Company Ticker"
              />
            )}
            onChange={(event, value) => {
              console.log(value);
              setSelectedCompetitorTickers(value.map((v) => v.ticker));
            }}
          />
        </Stack>
      </div>
      <div className="flex justify-center items-center">
        <button
          onClick={handleButtonClick}
          className="bg-[#3AABD4] hover:bg-blue-700 items-center text-white font-bold py-2 px-4 rounded-2xl"
        >
          Calculate Forecast
        </button>
      </div>
      <div className="px-64 py-16">
        <div className="px-12 justify-center w-1/3 h-72 shadow-lg rounded-xl py-4">
          <p>Sentimental Analysis Score - </p>
          <div className="px-8 py-8">
            <CircularProgress progress={75} size={150} />
          </div>
        </div>
      </div>
    </>
  );
}
