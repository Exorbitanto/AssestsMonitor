from bs4 import BeautifulSoup
import requests

debank_prefix = "https://debank.com/profile/"

def get_soup_for_query(query):
    response = requests.get(query, headers={
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}
                            )
    return BeautifulSoup(response.content)


def validate_debank_wallet(debank_wallet):
    soup = get_soup_for_query(f"{debank_prefix}{debank_wallet}")
    print(get_data_from_soup(soup))

def get_data_from_soup(soup):
    return soup.find('div', {'class': 'HeaderInfo_totalAsset__2noIk'})


validate_debank_wallet("0x09d4083ffd20d21acb9118465ad7c52ac8b548f7")
