import tls_client
import random

# Work on proper TLS connections such as JA3, etc

class TLSClient:
    def __init__(self):
        self.session = self.create_session()
        self.proxies = self.load_proxies()

    def create_session(self):
        # Change this so it can get the value of the user-agent and set the identifier based on it.
        # For now, use default chrome_117
        session = tls_client.Session(client_identifier = "chrome_117", random_tls_extension_order = True)
        session.headers = self.get_base_headers()
        return session

    def load_proxies(self):
        with open("proxies.txt", "a+") as file:
            file.seek(0, 0)
            return file.read().splitlines()

    def update_session_proxy(self):
        if (self.proxies):
            proxy = random.choice(self.proxies)
            self.session.proxies.update({"http": "http://" + proxy, "https": "http://" + proxy})

    def get_base_headers(self):
        return {
            "Host": self.site_url,
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Origin": "https://" + self.site_url,
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://" + self.site_url,
            "Accept-Language": "en-US,en;q=0.9",
        }