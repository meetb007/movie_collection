import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

MAX_RETRY_COUNT = 3

BACKOFF_FACTOR_IN_SECONDS = 120

FAILURE_STATUS_CODES = [
    500,
    502,
    503,
    504
]


def requests_retry_session(
    retries=MAX_RETRY_COUNT,
    backoff_factor=BACKOFF_FACTOR_IN_SECONDS,
    status_forcelist=FAILURE_STATUS_CODES,
    session=None,
):
    session = session or requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_with_retry(*args, **kwargs):
    return requests_retry_session().get(*args, **kwargs, verify=False)


def post_with_retry(*args, **kwargs):
    return requests_retry_session().post(*args, **kwargs, verify=False)


def get(*args, **kwargs):
    return requests.get(*args, **kwargs, verify=False)


def post(*args, **kwargs):
    return requests.post(*args, **kwargs, verify=False)


def request(*args, **kwargs):
    return requests.request(*args, **kwargs, verify=False)
