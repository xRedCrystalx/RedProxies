import sys, aiohttp, re, json, typing
sys.dont_write_bytecode = True

# global scraper class for websites, used by other scrapers
# this scraper can find IPv4 and IPv6 addresses with PORTs that are listed on website using regex
class Scraper:
    def __init__(self, url: str, protocol: str, session: aiohttp.ClientSession) -> None:
        self.url: str = url
        self.session: aiohttp.ClientSession = session
        self.protocol: str = protocol
        self.IPs: list[str] = []
        
        # constants for IP searching
        self.constants: dict[str, re.Pattern | list[str | re.Pattern]] = {
            "IPTypes" : ["ip", "host", "address", "ipv4", "ipv6", "ip4", "ip6", "ips"],
            "PortTypes" : ["port", "portnumber", "gate"],
            "ProtocolTypes" : ["protocol", "type", "prot"],

            "PROTOCOLS" : ["ssl", "secure", "socks", "http", "https", "socks4", "socks5"],
            
            "IPv4" : re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"),
            "IPv4+PORT" : re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b"),
            
            "IPv6": re.compile(r"\b(?:\[?[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]?\b"),
            "IPv6+PORT": re.compile(r"\b(?:\[?[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]?:[0-9]+\b"),
            
            "PORT" : re.compile(r"\b(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])\b"),
        }

    # async method that requests data from the given link
    async def request(self) -> str:
        response: aiohttp.ClientResponse = await self.session.get(self.url)
        return await response.text(encoding="utf-8")

    # async data handling method, changed by other *Scraper classes.
    # Searches for IPv4 and IPv6 addresses with PORTs and converts them in IPAddress object
    async def handler(self, text: str) -> None:
        #IPv4 regex - 192.168.1.1:8080
        IPv4: list[str] = self.constants["IPv4+PORT"].findall(string=text) 
        if IPv4:
            self.IPs.extend(IPv4)

        #IPv6 regex - 2001:db8::1:8080 or [3ffe:1900:4545:3:200:f8ff:fe21:67cf]:12345
        IPv6: list[str] = self.constants["IPv6+PORT"].findall(string=text)
        if IPv6:
            self.IPs.extend(IPv6)
    
    # main callable method, requests, handles and returns data with error handling
    async def scrape(self) -> list[str]:
        """Start scraper class with this method. Requires 0 arguments."""
        print(f"Scraping {self.url}")
        try:
            response: str = await self.request()
            await self.handler(text=response)
        except Exception as error:
            raise error

        return self.IPs

# requires update later
class TableScraper(Scraper):
    async def handler(self, text: str) -> None:
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

# json scraper class, equals to **Scraper**, changes searching functionality

class JSONScraper(Scraper):
    # dict walker, recursevly walks through the dict
    def dict_walker(self, json_dict: dict[str, typing.Any]) -> None:
        for key, value in json_dict.items():
            # if key == ip type name, check for matches -> {"IPv4" : ["ip1", "ip2", "ip3"]}
            if self.key_check(key.lower(), "IPTypes") and isinstance(value, (dict, list, tuple)):
                for IP in value:
                    self.get_matches(IP)
            
            # protocols handler -> {"http" : ["ip1", "ip2", "ip3"]}
            elif self.key_check(key.lower(), "PROTOCOLS") and isinstance(value, (dict, list, tuple)):
                if key.lower() == self.protocol.lower():
                    for PROTOCOL in value:
                        self.get_matches(PROTOCOL)

            # unknown, search more
            elif isinstance(value, dict):
                self.dict_walker(value)

            # unknown, check matches
            elif isinstance(value, (list, tuple)):
                if isinstance(value[0], str):
                    self.get_matches(item)
                else:
                    for item in value:
                        self.get_matches(item)

            # NOTE: handle dict[str, dict], ipv6

    
    def get_matches(self, request: dict[str, typing.Any] | str | list[dict | str]) -> None:
        if isinstance(request, dict):
            IP: str = ":"
            for key, value in request.items():
                if self.key_check(key.lower(), "ProtocolTypes") and str(value).lower() != self.protocol:
                    break

                elif self.key_check(key.lower(), "IPTypes"):
                    full_ips: list[str] | None = self.value_check(self.constants["IPv4+PORT"], value) or self.value_check(self.constants["IPv6+PORT"], value)
                    if full_ips:
                        IP = full_ips[0]
                        continue
                
                    ip_only: list[str] | None = self.value_check(self.constants["IPv4"], value) or self.value_check(self.constants["IPv6"], value)
                    if ip_only:
                        IP = ip_only[0] + IP

                elif self.key_check(key.lower(), "PortTypes"):
                    port: list[str] | None = self.value_check(self.constants["PORT"], value)
                    if port:
                        IP += port[0]
            else:
                data = self.value_check(self.constants["IPv4+PORT"], IP) or self.value_check(self.constants["IPv6+PORT"], IP)
                if data:
                    self.IPs.extend(data)
        
        elif isinstance(request, (list, tuple)):
            for item in request:
                data: list[str] | None = self.value_check(self.constants["IPv4+PORT"], item) or self.value_check(self.constants["IPv6+PORT"], item)
                if data:
                    self.IPs.extend(data)
        else:
            data: list[str] | None = self.value_check(self.constants["IPv4+PORT"], request) or self.value_check(self.constants["IPv6+PORT"], request)
            if data:
                self.IPs.extend(data)
            
    def key_check(self, key: str, constant: str) -> None:
        return key in self.constants.get(constant)

    def value_check(self, pattern: re.Pattern, string: str) -> list[str] | None:
        return pattern.findall(string) or None

    # replacing handler method with new one for searching
    # this handler is programmed to try and figure out what JSON object it got and create IP:PORT matches with filtered requests
    # handler might not be able to handle every kind of provided JSON object
    async def handler(self, text: str) -> str:
        # decoding attempt
        try:
            decodedJSON: dict = json.loads(text)
        except Exception:
            try:
                decodedJSON: dict = json.load(text)
            except Exception:
                print(f"JSONScraper failed to decode data of {self.url} website. -- Attempting to perform normal Scraper attempt.")
                # if it fails, we attempt to search for IPs with basic scraper
                return
        
        # successful decoding
        # now we have to figure out structure
        self.dict_walker(decodedJSON)
        return self.IPs
