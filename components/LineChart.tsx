import React, { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export function LineChart({ tickers }) {
  const [chartData, setChartData] = useState([]);
  const [labels, setLabels] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [colors, setColors] = useState([
    "#03045e",
    "#023e8a",
    "#0077b6",
    "#0096c7",
    "#00b4d8",
    "#48cae4",
    "#90e0ef",
    "#ade8f4",
    "#caf0f8",
    "#03045e",
  ]);

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: `DCF Valuation`,
      },
    },
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (!Array.isArray(tickers) || tickers.length === 0) {
          console.error("No tickers provided.");
          return;
        }

        const tickersArray = tickers.slice(0, 5); // Limit to a maximum of 5 tickers

        const fetchPromises = tickersArray.map(async (ticker) => {
          const response = await fetch(
            `http://127.0.0.1:5000/predict/${ticker}`
          );
          if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
          }
          return response.json();
        });

        const responseData = await Promise.all(fetchPromises);

        if (responseData.length > 0) {
          // Combine data from all tickers into a single dataset
          const combinedData = responseData.map((data, index) => ({
            label: tickersArray[index],
            data: data.map((item) => item.value),
            borderColor: `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${
              Math.random() * 255
            })`,
            backgroundColor: `rgba(${Math.random() * 255}, ${
              Math.random() * 255
            }, ${Math.random() * 255}, 0.5)`,
          }));

          setLabels(responseData[0].map((item) => item.date));
          setDatasets(combinedData);

          console.log("Data fetched successfully");
          console.log(responseData);
        } else {
          console.error("No data fetched for any tickers.");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [tickers]);

  const data = {
    labels,
    datasets,
  };

  return <Line options={options} data={data} />;
}
