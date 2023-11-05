import { Inter } from "next/font/google";
import * as React from "react";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import { useState } from "react";
import Stack from "@mui/material/Stack";

const inter = Inter({ subsets: ["latin-ext"] });

const inputStyle = {
  color: "white",
};

// const companyTickers = [
//   { name: "Apple", ticker: "AAPL" },
//   { name: "Goldman Sachs", ticker: "GS" },
//   { name: "Microsoft", ticker: "MSFT" },
// ];

export default function Home() {
  // pull in the company tickers from the database
  const [companyTickers, setCompanyTickers] = useState([
    { name: "Apple", ticker: "AAPL" },
  ]);
  const [selectedTicker, setSelectedTicker] = useState("AAPL");

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
      {/* COMPLETED */}
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
          getOptionLabel={(option) => option.ticker} // Display the name in the input field
          renderInput={(params) => (
            <TextField {...params} label="Company Ticker" variant="outlined" />
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
    </>
  );
}
