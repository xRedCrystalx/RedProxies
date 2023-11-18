import sys, aiohttp, dataclasses, re
sys.dont_write_bytecode = True

# global IP dataclass
@dataclasses.dataclass
class IPAddress:
    IPv4: str | None = None
    IPv6: str | None = None
    PORT: int = None

    def __post_init__(self) -> None:
        if self.IPv4 and self.IPv6:
            raise AttributeError("IPv4 and IPv6 cannot be filled at the same time.")
        elif not self.IPv4 and not self.IPv6:
            raise AttributeError("IPv4 or IPv6 must be filled.")

    def __str__(self) -> str:
        if self.IPv4:
            return f"{self.IPv4}:{self.PORT}"
        elif self.IPv6:
            return f"[{self.IPv6}]:{self.PORT}"

    def __repr__(self) -> str:
        if self.IPv4:
            return f"{self.IPv4}:{self.PORT}"
        elif self.IPv6:
            return f"[{self.IPv6}]:{self.PORT}"

# global scraper object for websites with API
class Scraper:
    def __init__(self, url: str, session: aiohttp.ClientSession) -> None:
        self.url: str = url
        self.session: aiohttp.ClientSession = session
        self.IPs: list[IPAddress] = []

    async def request(self) -> aiohttp.ClientResponse:
        return await self.session.get(self.url)

    async def handler(self, response: aiohttp.ClientResponse) -> str:
        return await response.text(encoding="utf-8")

    async def scrape(self) -> list[IPAddress]:
        print(f"Scraping {self.url}")
        try:
            response: aiohttp.ClientResponse = await self.request()
            text: str = await self.handler(response=response)
        except Exception as error:
            print(error)
            raise error

        #IPv4 regex - 192.168.1.1:8080
        IPv4: list[str] = re.findall(pattern=r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b", string=text, flags=re.IGNORECASE)
        if IPv4:
            self.IPs.extend([IPAddress(IPv4=IP.split(":")[0], PORT=int(IP.split(":")[1])) for IP in IPv4])

        #IPv6 regex - 2001:db8::1:8080 or [3ffe:1900:4545:3:200:f8ff:fe21:67cf]:12345
        IPv6: list[str] = re.findall(pattern=r"\b(?:\[?[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]?:[0-9]+\b", string=text, flags=re.IGNORECASE)
        if IPv6:
            self.IPs.extend([IPAddress(IPv6=IP.split("]:")[0].replace("[", ''), PORT=int(IP.split("]:")[1])) for IP in IPv6])

        return self.IPs

# requires update later
class TableScraper(Scraper):
    async def handler(self, response: aiohttp.ClientResponse) -> str:
        print("Table scraper is currently work in progress.")
        return 
        """
        table_pattern: re.Pattern[str] = re.compile(r'<table[^>]*class=["\']table table-striped table-bordered["\'][^>]*>.*?</table>', re.DOTALL)
        row_pattern: re.Pattern[str] = re.compile(r'<tr[^>]*>.*?</tr>', re.DOTALL)
        cell_pattern: re.Pattern[str] = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)
        print("compiled")
        html_code: str = await response.text(encoding="utf-8")
        table_match: re.Match[str] | None = table_pattern.search(html_code)
        proxies = set()
        print("vars set")

        if table_match:
            table_html: str = table_match.group(0)
            print("Table found!")
            for row_match in row_pattern.finditer(table_html):
                proxy: str = ":".join(cell.group(1).replace("&nbsp;", "") for cell in cell_pattern.finditer(row_match.group(0))[:2])
                proxies.add(proxy)

        return "\n".join(proxies)
    """