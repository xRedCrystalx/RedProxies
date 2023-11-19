import sys, aiohttp, dataclasses, re, json
sys.dont_write_bytecode = True

# global IP dataclass
@dataclasses.dataclass
class IPAddress:
    IPv4: str | None = None
    IPv6: str | None = None
    PORT: int = None

    # post initializer, checks if both versions of IPs were inputed and/or if any.
    def __post_init__(self) -> None:
        if self.IPv4 and self.IPv6:
            raise AttributeError("IPv4 and IPv6 cannot be filled at the same time.")
        elif not self.IPv4 and not self.IPv6:
            raise AttributeError("IPv4 or IPv6 must be filled.")

    # string method to handle print statements
    def __str__(self) -> str:
        if self.IPv4:
            return f"{self.IPv4}:{self.PORT}"
        elif self.IPv6:
            return f"[{self.IPv6}]:{self.PORT}"

    # repr method to handle file writes
    def __repr__(self) -> str:
        if self.IPv4:
            return f"{self.IPv4}:{self.PORT}"
        elif self.IPv6:
            return f"[{self.IPv6}]:{self.PORT}"

# global scraper class for websites, used by other scrapers
# this scraper can find IPv4 and IPv6 addresses with PORTs that are listed on website using regex
class Scraper:
    def __init__(self, url: str, session: aiohttp.ClientSession) -> None:
        self.url: str = url
        self.session: aiohttp.ClientSession = session
        self.IPs: list[IPAddress] = []
        
        # constants for IP searching
        self.constants: dict[str, re.Pattern | list[str | re.Pattern]] = {
            "IPTypes" : ["ip", "host", "address", "ipv4", "ipv6"],
            "PortTypes" : ["port", "portnumber", "gate"],
            
            "IPv4" : re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"),
            "IPv4+PORT" : re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b"),
            
            "IPv6": re.compile(r"\b(?:\[?[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]?\b"),
            "IPv6+PORT": re.compile(r"\b(?:\[?[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]?:[0-9]+\b"),
            
            "PORT" : re.compile(r"\b(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])\b"),
            "PROTOCOLS" : ["ssl", "secure", "socks", "http", "https", "socks4", "socks5"]
        }

    # async method that requests data from the given link
    async def request(self) -> str:
        response: aiohttp.ClientResponse = await self.session.get(self.url)
        return await response.text(encoding="utf-8")

    # async data handling method, changed by other *Scraper classes.
    # Searches for IPv4 and IPv6 addresses with PORTs and converts them in IPAddress object
    async def handler(self, text: str) -> None:
        #IPv4 regex - 192.168.1.1:8080
        IPv4: list[str] = re.findall(pattern=self.constants["IPv4+PORT"], string=text)
        if IPv4:
            self.IPs.extend([IPAddress(IPv4=IP.split(":")[0], PORT=int(IP.split(":")[1])) for IP in IPv4])

        #IPv6 regex - 2001:db8::1:8080 or [3ffe:1900:4545:3:200:f8ff:fe21:67cf]:12345
        IPv6: list[str] = re.findall(pattern=self.constants["IPv6+PORT"], string=text)
        if IPv6:
            self.IPs.extend([IPAddress(IPv6=IP.split("]:")[0].replace("[", ''), PORT=int(IP.split("]:")[1])) for IP in IPv6])
    
    # main callable method, requests, handles and returns data with error handling
    async def scrape(self) -> list[IPAddress]:
        """Start scraper class with this method. Requires 0 arguments."""
        print(f"Scraping {self.url}")
        try:
            response: str = await self.request()
            await self.handler(text=response)
        except Exception as error:
            print(error)
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
    
class JSONScraper(Scraper):
    async def handler(self, text: str) -> str:
        print("JSON Scraper is currently work in progress")
        #return
        
        # decoding attempt
        try:
            decodedJSON: dict = json.loads(text)
        except Exception:
            try:
                decodedJSON: dict = json.load(text)
            except Exception:
                print(f"JSONScraper failed to decode data of {self.url} website. -- Attempting to perform normal Scraper attempt.")
                await Scraper(url=self.url, session=self.session).scrape()
                return
        
        # successful decoding
        # now we have to figure out structure
        check: dict[str, bool] = {
            "IP" : False,
            "PORT" :  False,
            "TYPE" : False
        }
        
        def recursive_checking(data: dict, index: int) -> None:
            for key, value in list(data.items())[index:]:
                if isinstance(value, list):
                    for v in value:
                        recursive_checking(data=data, index=index+1)
                    break
                elif isinstance(value, dict):
                    ...
                
                else:
                    index += 1
        
        for key, value in self.constants.items():
            if isinstance(value, list):
                # here are three posibilities, list of IP:PORT (str) or list of dict or list of lists
                # lets check if the first argument is string
                if isinstance(value[0], str):
                    # now, we search for IPv4 and IPv6 IPs with port and extend to database
                    for regex in ["IPv4+PORT", "IPv6+PORT"]:
                        self.IPs.extend(re.findall(pattern=self.constants[regex], string=text, flags=re.IGNORECASE))
                
                # checking if the first value is dict
                elif isinstance(value[0], dict):
                    ...
                
                # checking if the first value is list
                # here, only logical posibility is to have multiple lists for each IP version (IPv4 and IPv6)
                # or lists of different protocols (HTTP, HTTPS, SOCKS...)
                elif isinstance(value[0], list):
                    # im going to use len() to figure out if its versions (2) or protocols (2+)
                    # versions:
                    if list_len := len(value) == 2:
                        for regex in ["IPv4+PORT", "IPv6+PORT"]:
                            self.IPs.extend(re.findall(pattern=self.constants[regex], string=text, flags=re.IGNORECASE))
                    # list is empty returning
                    elif list_len == 0:
                        return "List is empty."
                    
                    # protocols:
                    else:
                        ...
                
                # else, we can't really find anything else, so returning
                else:
                    print(f"Couldn't gather any data from: {self.url}")
                    return
                
            elif isinstance(value, dict):
                ...
            else:
                # if value is string, bool, int, float - there is no way of IP addresses being stored
                print(f"Couldn't find any IP address for url: {self.url}")
                return
