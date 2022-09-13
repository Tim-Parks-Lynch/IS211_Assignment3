import argparse
import requests
import csv
import io
import re


def download_data(url):
    response = requests.get(url)
    return response.text


def process_data_image_hits(data):
    image_hits = 0

    # Convert to CSV Data
    csv_data = csv.reader(io.StringIO(data))

    # Find image count and browsers
    for i, row in enumerate(csv_data):
        path = row[0]

        # Exclude .css and .html pages from search
        if re.search("gif|jpg|jpeg|png", path.lower()):
            image_hits += 1

    average_image_hits = image_hits / (i + 1) * 100
    return average_image_hits


def process_data_most_used_browser(data):
    browser_dict = {
        "IE": 0,
        "Safari": 0,
        "Chrome": 0,
        "Firefox": 0,
    }

    csv_data = csv.reader(io.StringIO(data))

    # User Agent Codes
    # Firefox = Firefox only
    # Chrome = Chrome and Safari
    # IE = MSIE or Trident
    # Safari = Safari on it's own, no chrome
    for row in csv_data:
        browser = row[2]
        if re.search("MSIE", browser):
            browser_dict["IE"] += 1
        elif re.search("Firefox", browser):
            browser_dict["Firefox"] += 1
        elif re.search("Chrome", browser):
            browser_dict["Chrome"] += 1
        else:
            browser_dict["Safari"] += 1

    most_used_browser = max(browser_dict, key=browser_dict.get)
    return most_used_browser


def display_data(*args):
    print(
        f"Image requests account for {args[0]}% of all requests, and {args[1]} is the most popular browser"
    )


def main(url):
    data = download_data(url)
    image_hits = process_data_image_hits(data)
    most_used_browser = process_data_most_used_browser(data)
    display_data(image_hits, most_used_browser)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", help="URL to the datafile", type=str, required=True
    )
    args = parser.parse_args()
    main(args.url)
