import requests.exceptions

HTTPApiException = (requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.HTTPError)
