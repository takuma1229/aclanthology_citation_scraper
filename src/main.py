import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import argparse
from tqdm import tqdm

class ACLAnthologyScraper:
    def __init__(self, conference, year):
        self.conference = conference
        self.year = year
        self.base_url = f"https://aclanthology.org/events/{conference}-{year}/"
        self.papers = []
        self.paper_citations = []

    def fetch_url(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def extract_papers(self):
        soup = self.fetch_url(self.base_url)
        for paper in soup.find_all('p', class_='d-sm-flex align-items-stretch'):
            title_tag = paper.find('strong')
            if title_tag:
                title = title_tag.text.strip()
                if 'proceedings' in title.lower():
                    continue
                link_tag = title_tag.find('a', href=True)
                if link_tag:
                    link = link_tag['href']
                    self.papers.append((title, link))

    def get_doi(self, detail_page_url):
        soup = self.fetch_url(detail_page_url)
        doi_tag = soup.find('a', title="To the current version of the paper by DOI")
        return doi_tag.text.strip() if doi_tag else None

    def get_citations(self, doi):
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['message'].get('is-referenced-by-count', 0)
        return 0

    def fetch_paper_details(self):
        for title, link in tqdm(self.papers, desc="Fetching paper details"):
            detail_page_url = f"https://aclanthology.org{link}"
            doi = self.get_doi(detail_page_url)
            if doi:
                citations = self.get_citations(doi)
                self.paper_citations.append((title, doi, citations))
                time.sleep(1)  # リクエスト間隔を空けるためのウェイト
            else:
                self.paper_citations.append((title, None, 0))

    def save_to_csv(self):
        df = pd.DataFrame(self.paper_citations, columns=['Title', 'DOI', 'Citations'])
        df_sorted = df.sort_values(by='Citations', ascending=False)
        output_filename = f'./output/{self.conference}_{self.year}_papers.csv'
        df_sorted.to_csv(output_filename, index=False)
        print(df_sorted)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape ACL Anthology for papers.')
    parser.add_argument('conference', type=str, help='The conference acronym (e.g., acl, naacl)')
    parser.add_argument('year', type=int, help='The year of the conference (e.g., 2023)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    scraper = ACLAnthologyScraper(args.conference, args.year)
    scraper.extract_papers()
    scraper.fetch_paper_details()
    scraper.save_to_csv()

if __name__ == '__main__':
    main()
