import requests
from json import JSONDecodeError


def _get_access_token(key, secret):
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


def main():
    pass


if __name__ == "__main__":
    main()

