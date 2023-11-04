import requests
import json

CIK = "0000886982"
SUBMISSIONS_ENDPOINT = f"https://data.sec.gov/submissions/CIK{CIK}.json"

response = requests.get(SUBMISSIONS_ENDPOINT, headers={"User-Agent": "Mozilla/5.0"})

if response.status_code == 200:
    data = response.json()

    filings_data = data.get("filings", {}).get("recent")
    
    edited_data = {"cik": data.get("cik"), "filings": filings_data}

    report_date = edited_data.get("filings").get("reportDate")
    parsed_date = []

    # In all report dates save the index of the non blank report_dates
    for index, date in enumerate(report_date):
        if date:
            parsed_date.append(index)
        
    # Save all ascenion numbers in an object with corresponding indexes from parsed_data
    accession_numbers = []

    for index in parsed_date:
        accession_numbers.append({
            "number": edited_data.get("filings").get("accessionNumber")[index],
            "index": index,
            "date": edited_data.get("filings").get("reportDate")[index],
            "form": edited_data.get("filings").get("form")[index]
        })

    # Remove all forms that are not 10-K or 10-Q
    accession_numbers = [accession_number for accession_number in accession_numbers if accession_number["form"] in ["10-K", "10-Q"]]

    # In all accession numbers remove the - 
    for accession_number in accession_numbers:
        accession_number["number"] = accession_number["number"].replace("-", "")

    edited_data = accession_numbers
    
    with open(f"CIK{CIK}.json", "w") as f:
        json.dump(edited_data, f, indent=4)
    
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

from bs4 import BeautifulSoup as bs

HTML_ENDPOINT = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{edited_data[0]['number']}/R4.htm"

response = requests.get(HTML_ENDPOINT, headers={"User-Agent": "Mozilla/5.0"})

if response.status_code == 200:
    soup = bs(response.text, "html.parser")

    print(soup.prettify())

    # Get the table with the financial data
    table = soup.find("table", {"class": "report"})

    # Get all rows from the table
    rows = table.find_all("tr")

    # Get all columns from the table
    columns = [row.find_all("td") for row in rows]

    # Get all the text from the columns
    text = [[column.get_text() for column in row] for row in columns]

    # Remove all empty lists
    text = [row for row in text if row]

    # Remove all empty strings
    text = [[column for column in row if column] for row in text]

    # Remove all \xa0
    text = [[column.replace("\xa0", "") for column in row] for row in text]

    # Remove all \n
    text = [[column.replace("\n", "") for column in row] for row in text]

    # Remove all \t
    text = [[column.replace("\t", "") for column in row] for row in text]

    # Remove all spaces
    text = [[column.strip() for column in row] for row in text]

    # Remove all empty strings
    text = [[column for column in row if column] for row in text]

    # Remove all empty lists
    text = [row for row in text if row]

    print(text)

    # save the data in a json file
    with open(f"CIK{CIK}_{edited_data[0]['number']}.json", "w") as f:
        json.dump(text, f, indent=4)

    print(HTML_ENDPOINT)

    print(edited_data[0]['form'])

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")