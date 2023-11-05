import { Inter } from "next/font/google";
import * as React from "react";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import { useState } from "react";
import Stack from "@mui/material/Stack";
import Image from "next/image";
import { LineChart } from "../components/LineChart";
import CircularProgress from "./components";
import { Header } from "@/components/Header";
import { JPM, CBRE } from "./compsend";

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
  const [companyTickers, setCompanyTickers] = useState([
    { name: "Apple", ticker: "AAPL" },
    { name: "Goldman Sachs", ticker: "GS" },
    { name: "Microsoft", ticker: "MSFT" },
  ]);
  const [selectedTicker, setSelectedTicker] = useState("GS");
  const [selectedCompetitorTickers, setSelectedCompetitorTickers] = useState([
    "GS",
  ]);
  const [sentiment, setSentiment] = useState(67);

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
    <div className="">
      <div>
        <div>
          <div className="flex items-center justify-center text-center">
            <img src="logo.svg" alt=""></img>
          </div>
          <div className="mb-10 m-auto items-center flex justify-center">
            <Header ticker={selectedTicker} />
          </div>
        </div>
      </div>

      <div className="flex justify-center gap-x-20 mt-10">
        <Autocomplete
          disablePortal
          id="combo-box-demo"
          options={companyTickers}
          //defaultValue={companyTickers[0]}
          sx={{ width: 200 }}
          getOptionLabel={(option) => option.ticker}
          onChange={(event, data) => {
            setSelectedTicker([data.ticker]);

            console.log(selectedTicker);
            fetch("http://127.0.0.1:5000/sentiment/" + selectedTicker).then(
              (response) => {
                response.json().then((data) => {
                  setSentiment(Math.round(data.percent * 100));
                });
              }
            );
          }}
          renderInput={(params) => {
            const selectedOption = companyTickers.find((option) => {
              option.ticker === selectedTicker;
            });
            return (
              <div style={{ display: "flex", alignItems: "center" }}>
                <TextField
                  {...params}
                  label="Company Ticker"
                  variant="outlined"
                  value={selectedOption ? selectedOption.ticker : ""}
                  style={{ flex: 1 }} // Expand to fill the remaining space
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
        <Stack spacing={3} sx={{ width: 200 }}>
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
      <div className="px-24 py-8 flex justify-items">
        <div className="mt-20 justify-center w-auto h-72 rounded-xl py-4">
          <p className="py-2 px-16 w-72 text-center mt-4">
            Sentimental Analysis
          </p>
          <div className="px-24 py-12">
            <CircularProgress progress={sentiment} size={100} />
          </div>
        </div>
        <div className="flex justify-center items-center">
          {/* <button
            onClick={handleButtonClick}
            className="bg-[#3AABD4] hover:bg-blue-700 items-center text-white font-bold py-2 px-4 rounded-2xl"
          >
            Calculate Forecast
          </button> */}
        </div>
        <div className="w-full">
          <LineChart tickers={selectedCompetitorTickers} />
        </div>
      </div>
      <div>
        <CBRE />
      </div>
    </div>
  );
}
