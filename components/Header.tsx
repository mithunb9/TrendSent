import React, { useEffect, useState } from "react";
import Image from "next/image";

export function Header({ ticker }) {
  const [companyData, setCompanyData] = useState<{ profile?: any }>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (!ticker) {
          console.error("No ticker provided.");
          return;
        }

        const response = await fetch(
          `https://financialmodelingprep.com/api/v4/company-outlook?symbol=${ticker}&apikey=Jggm58IcEjuNOgj5QPEy4Ykg4gCo5PtU`
        );

        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        setCompanyData(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, [ticker]);

  // Extract numeric parts
  const priceNumeric = parseFloat(companyData.profile?.price);
  const changesNumeric = Math.abs(parseFloat(companyData.profile?.changes)); // Use Math.abs to get the absolute value

  // Determine the color based on the changes
  const priceColorClass =
    parseFloat(companyData.profile?.changes) < 0
      ? "text-red-500"
      : "text-green-500";

  // Determine the arrow icon and its color
  const arrowIcon =
    parseFloat(companyData.profile?.changes) < 0 ? (
      <span className="text-red-500">&#9660;</span> // Red triangle pointing down
    ) : (
      <span className="text-green-500">&#9650;</span> // Green triangle pointing up
    );

  return (
    <>
      {companyData.profile && (
        <div className="flex flex-row space-x-2">
          <Image
            src={`/Logos/${ticker}.png`}
            alt="Logo"
            width={60}
            height={60}
          />
          <div>
            <h1 className="text-3xl">{companyData.profile.companyName}</h1>
            <div className="flex flex-row space-x-2">
              <h2 className="text-xl">${companyData.profile.symbol}</h2>
              <div className={`text-xl ${priceColorClass}`}>
                {priceNumeric.toFixed(2)}
              </div>
            </div>
          </div>
          <div className={`p-4 text-2xl ${priceColorClass}`}>
            <h1>
              <span className="p-2">{arrowIcon}</span>
              {changesNumeric.toFixed(2)}{" "}
            </h1>
          </div>
        </div>
      )}
    </>
  );
}
