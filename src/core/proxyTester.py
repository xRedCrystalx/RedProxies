import sys, aiohttp, re, typing, time
sys.dont_write_bytecode = True
from src.runner import IPv4p, IPv6p, connector

class Tester:
    def __init__(self, protocol: str, proxy: str, user_agent: str) -> None:
        self.protocol: str = protocol
        self.proxy: str = str(proxy)
        self.user_agent: str = user_agent
        
        if not self.isValid():
            raise ValueError("Provided IP address is not valid.")
    
    def isValid(self) -> str | None:
        v4: re.Match[str] | None = IPv4p.search(string=self.proxy)
        v6: re.Match[str] | None = IPv6p.search(string=self.proxy)
        
        return "IPv4" if v4 else "IPv6" if v6 else None
    
    async def check(self) -> str | bool:
        pass
    
    def __str__(self) -> str:
        return self.proxy
    
    def __repr__(self) -> str:
        return self.proxy
    
class HTTPtester(Tester):
    async def check(self, timeout: float) -> str | bool:
        params: dict[str, typing.Any] = {
            "timeout" : aiohttp.ClientTimeout(total=timeout),
            "headers" : {"User-Agent" : self.user_agent},
        }
        async with aiohttp.ClientSession(**params) as session:
            start: float = time.perf_counter()
            
            if self.protocol == "http":
                url: str = connector.config["Configuration"]["testerDefaultWebsiteHTTP"]
            elif self.protocol == "https":
                url: str = connector.config["Configuration"]["testerDefaultWebsiteHTTPS"]
            else:
                return
 
            try:
                async with session.get(url=url, proxy=f"{self.protocol}://{self.proxy}") as response:
                    pass
            except Exception:
                return False

        if response.status != 200:
            return False
        
        self.time: int = int((time.perf_counter() - start) * 1000)
        
        return self.proxy
            
            