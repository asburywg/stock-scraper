import logging
import time
import requests

log = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def fetch(url, retries=0, max_retries=3):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    try:
        return requests.get(url, timeout=10, headers={"User-Agent": ua})
    except:
        if retries < max_retries:
            log.debug(f"Retry {retries + 1}: {url}")
            time.sleep(3)
            fetch(url, retries + 1)
        else:
            log.debug(f"Failed: {url}")
            return None
