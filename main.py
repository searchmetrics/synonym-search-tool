import requests
from json import JSONDecodeError
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
    return get_keyword_info(keyword)[0]["search_volume"]


def main():
    info = get_keyword_search_volume("metallica")
    print(info)


if __name__ == "__main__":
    main()
