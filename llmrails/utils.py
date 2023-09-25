from requests import Response
from requests.exceptions import HTTPError
from llmrails.exceptions import RequestException


def get_error_message(response: Response):
    try:
        content = response.json()
        if content.get('error'):
            return content['error']['message']
        
    except Exception:
        return response.reason



def raise_for_status(response: Response):
    try:
        response.raise_for_status()
    except HTTPError:
        err_msg = get_error_message(response)
        raise RequestException(f"{response.status_code} Server Error: {err_msg} for url: {str(response.url)}")
    except Exception as e:
        raise e