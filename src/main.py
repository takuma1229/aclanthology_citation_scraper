import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import argparse

# 引数のパーサーを設定
parser = argparse.ArgumentParser(description='Scrape ACL Anthology for papers.')
parser.add_argument('conference', type=str, help='The conference acronym (e.g., acl, naacl)')
parser.add_argument('year', type=int, help='The year of the conference (e.g., 2023)')

# 引数を解析
args = parser.parse_args()
conference = args.conference
year = args.year

# ACL Anthologyの特定のイベントURLを生成
url = f"https://aclanthology.org/events/{conference}-{year}/"

# ウェブページの内容を取得
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 論文のタイトルと詳細ページへのリンクを抽出
papers = []
for paper in soup.find_all('p', class_='d-sm-flex align-items-stretch'):
    title_tag = paper.find('strong')
    if title_tag:
        title = title_tag.text.strip()
        if 'proceedings' in title.lower():
            continue
        link_tag = title_tag.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            papers.append((title, link))

# 各論文の詳細ページからDOIを取得する関数
def get_doi(detail_page_url):
    response = requests.get(detail_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    doi_tag = soup.find('a', title="To the current version of the paper by DOI")
    if doi_tag:
        return doi_tag.text.strip()
    return None

# CrossRef APIを使って被引用数を取得する関数
def get_citations(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['message'].get('is-referenced-by-count', 0)
    return 0

# 論文のタイトル、DOI、被引用数を取得
paper_citations = []
for title, link in papers:
    detail_page_url = f"https://aclanthology.org{link}"
    doi = get_doi(detail_page_url)
    if doi:
        citations = get_citations(doi)
        paper_citations.append((title, doi, citations))
        time.sleep(1)  # リクエスト間隔を空けるためのウェイト
    else:
        paper_citations.append((title, None, 0))

# データフレームに変換し、被引用数順にソート
df = pd.DataFrame(paper_citations, columns=['Title', 'DOI', 'Citations'])
df_sorted = df.sort_values(by='Citations', ascending=False)

# CSVファイルに保存
output_filename = f'./output/{conference}_{year}_papers.csv'
df_sorted.to_csv(output_filename, index=False)

# 結果を表示
print(df_sorted)
