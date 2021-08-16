from json import JSONDecodeError
import requests
import pandas as pd
from itertools import product
from re import findall

import secret_data


def get_access_token(key, secret):
    get_access_token_url = "https://api.searchmetrics.com/v4/token"
    r = requests.post(
        url=get_access_token_url,
        auth=(key, secret),
        data={"grant_type": "client_credentials"},
    )

    try:
        access_token = r.json()["access_token"]
        return access_token
    except (JSONDecodeError, KeyError) as err:
        raise Exception(
            f"SM API: Could not receive access token with credentials: {key} - {secret}. "
            f"Error message: {err}"
        )


def get_keyword_info(keyword, country_code="us"):
    get_keyword_info_url = "https://api.searchmetrics.com/v4/ResearchKeywordsGetListKeywordinfo.json"
    request_params = {
        "keyword": keyword,
        "countrycode": country_code,
        "access_token": get_access_token(secret_data.SM_API_KEY, secret_data.SM_API_SECRET),
    }
    r = requests.get(get_keyword_info_url, params=request_params)
    return r.json()["response"]


def get_keyword_search_volume(keyword, country_code="us"):
    return get_keyword_info(keyword, country_code)[0]["search_volume"]


def get_column_set(dataframe, keyword):
    x_set = set()
    for x in dataframe[keyword]:
        x_set.add(x)
    return x_set


def get_word_synonyms(df):
    word_synonyms = {}
    df_dict = df.to_dict()
    for key in df_dict:
        temp_dict = df_dict[key]
        for nested_key in temp_dict:
            if isinstance(temp_dict[nested_key], float):
                continue
            if nested_key in word_synonyms:
                word_synonyms[nested_key] += [temp_dict[nested_key].lower()]
            else:
                word_synonyms[nested_key] = [temp_dict[nested_key].lower()]
    return [[x] + word_synonyms[x] for x in word_synonyms]


def get_synonymic_phrases(phrase, word_synonyms):
    occurring_word_synonyms = []
    synonymic_phrases = []
    for word in findall(r'\w+', phrase):
        for word_synonym in word_synonyms:
            if word in word_synonym:
                phrase = phrase.replace(word, "{}", 1)
                occurring_word_synonyms.append(word_synonym)
                print(phrase, word)

    for i in product(*occurring_word_synonyms):
        synonymic_phrases.append(phrase.format(*i))

    return synonymic_phrases


def main():
    synonyms_file = pd.read_csv("sample_input_synonym_replacer.csv")
    phrases_file = pd.read_excel("sample_input_search_phrases.xlsx")
    phrases = get_column_set(phrases_file, "phrase")
    words = get_column_set(synonyms_file, "Words")

    phrases_with_keywords = set()
    for word in words:
        for phrase in phrases:
            if isinstance(word, str) and word in phrase:
                phrases_with_keywords.add(phrase)

    word_synonyms = get_word_synonyms(pd.read_csv("sample_input_synonym_replacer.csv", index_col=0, squeeze=False))

    synonymic_phrases = []
    for phrase in phrases_with_keywords:
        synonymic_phrases.append(get_synonymic_phrases(phrase, word_synonyms))


if __name__ == "__main__":
    main()
