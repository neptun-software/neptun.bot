import requests


def fetch_and_parse_proxies(url):
    response = requests.get(url)
    response.raise_for_status()

    content = response.text

    proxies = content.splitlines()

    return proxies


def should_abort_request(request):
    return (
        request.resource_type == "image"
        or ".jpg" in request.url or "font" in request.url
    )
