import os
from datetime import date

import requests
import pandas as pd
from bs4 import BeautifulSoup

from cowidev.utils.clean.dates import localdatenow


def main():
    url = "https://koronavirus.gov.mk/"
    location = "North Macedonia"
    output_file = f"automated_sheets/{location}.csv"

    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    count = int(soup.find_all("td")[7].text.replace(",", ""))
    # print(count)

    date_str = localdatenow("Europe/Skopje")
    df = pd.DataFrame(
        {
            "Country": location,
            "Date": [date_str],
            "Cumulative total": count,
            "Source URL": url,
            "Source label": "Ministry of Health",
            "Units": "tests performed",
            "Notes": pd.NA,
        }
    )

    if os.path.isfile(output_file):
        existing = pd.read_csv(output_file)
        if count > existing["Cumulative total"].max() and date_str > existing["Date"].max():
            df = pd.concat([df, existing]).sort_values("Date", ascending=False).drop_duplicates()
            df.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
