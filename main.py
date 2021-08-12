import requests
from json import JSONDecodeError
import secret_data
import pandas as pd


# def get_access_token(key, secret):
#     get_access_token_url = "https://api.searchmetrics.com/v4/token"
#     r = requests.post(
#         url=get_access_token_url,
#         auth=(key, secret),
#         data={"grant_type": "client_credentials"},
#     )
#
#     try:
#         access_token = r.json()["access_token"]
#         return access_token
#     except (JSONDecodeError, KeyError) as err:
#         raise Exception(
#             f"SM API: Could not receive access token with credentials: {key} - {secret}. "
#             f"Error message: {err}"
#         )
#
#
# def get_keyword_info(keyword, country_code="us"):
#     get_keyword_info_url = "https://api.searchmetrics.com/v4/ResearchKeywordsGetListKeywordinfo.json"
#     request_params = {
#         "keyword": keyword,
#         "countrycode": country_code,
#         "access_token": get_access_token(secret_data.SM_API_KEY, secret_data.SM_API_SECRET),
#     }
#     r = requests.get(get_keyword_info_url, params=request_params)
#     return r.json()["response"]
#
#
# def get_keyword_search_volume(keyword, country_code="us"):
#     return get_keyword_info(keyword)[0]["search_volume"]

def get_words(column):
    words = []
    for word in column:
        words.extend(word.split())
    return words


def main():
    file_name = "sample.xlsx"
    xlsx_file = pd.read_excel(file_name)
    phrases = xlsx_file["phrase"]
    print(get_words(phrases))


if __name__ == "__main__":
    main()
