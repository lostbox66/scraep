import argparse
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
import time


def extract_links(url, depth=0, max_depth=3, seen=None, results=None):
    if depth > max_depth:
        return
    if seen is None:
        seen = set()
    if results is None:
        results = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip() if soup.title else None
        if not title:
            return
        timestamp = int(time.time())
        print(f"{url} - {title}")
        results.append({'url': url, 'title': title, 'timestamp': timestamp})
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href is not None:
                absolute_url = urljoin(url, href)
                if absolute_url not in seen:
                    seen.add(absolute_url)
                    extract_links(absolute_url, depth=depth+1, max_depth=max_depth, seen=seen, results=results)
    except requests.exceptions.RequestException:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='the starting URL to extract links from')
    parser.add_argument('--depth', type=int, default=3, help='the maximum depth to crawl')
    parser.add_argument('--output', help='the output file to write the extracted URLs to (in JSON format)')
    args = parser.parse_args()

    start_url = args.url
    max_depth = args.depth
    output_file_path = args.output

    results = []
    try:
        extract_links(start_url, max_depth=max_depth, results=results)
    except KeyboardInterrupt:
        pass

    with open(output_file_path, 'w') as output_file:
        json.dump(results, output_file)


if __name__ == '__main__':
    main()
