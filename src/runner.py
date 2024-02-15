import sys, re, typing, aiohttp, platform
sys.dont_write_bytecode = True
import src.system.colors as colors
import src.core.websiteScraper as wScraper

if typing.TYPE_CHECKING:
    import src.core.cmds as cmds

IPv4p: re.Pattern[str] = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b")
IPv6p: re.Pattern[str]= re.compile(r"\b(?:\[?[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]?:[0-9]+\b")

class Connector:
    def __init__(self) -> None:
        self.path: str = None
        self.c: colors.C | colors.CNone = None
        self.config: dict = None
        self.OS: str = platform.system()
        self.cmd_class: cmds.Commands = None
        
        self.proxies: list[str] = []
        self.proxy_scrapers: list[wScraper.Scraper | wScraper.TableScraper] = []
        self.user_agents: list[str] | None = None
        self.session: aiohttp.ClientSession = None
        self.protocol: str = None
        self.output_file: str = None
        
        self._version: str = "v0.0.3"
        self._default_headers: dict[str, str] = {"User-Agent" : f"RedCrawler/{self._version} ({self.OS}; Python) aiohttp/{aiohttp.__version__}"}
        self._default_user_agent: str = f"RedCrawler/{self._version} ({self.OS}; Python) aiohttp/{aiohttp.__version__}"
    
    async def cmd_handler(self) -> None:
        def parser(cmd_str: str) -> list[str]:
            arguments: list[str] = []
            current_arg: str = ""
            inQuotes = False
            
            for char in cmd_str:
                if char == ' ' and not inQuotes:
                    if current_arg:
                        arguments.append(current_arg)
                        current_arg: str = ""
                elif char == '"':
                    inQuotes: bool = not inQuotes
                else:
                    current_arg += char

            if current_arg:
                arguments.append(current_arg)

            return arguments
        
        while True:
            try:
                cmd_request = str(input(f"{self.c.Red}RedProxies{self.c.R} > "))
            except Exception:
                await self.cmd_class._terminator()
            
            cmd: str = cmd_request.split(" ")[0]

            if [x for x in self.cmd_class.commands.keys() if cmd in x]:
                arguments: list[str] = parser(cmd_str=cmd_request)
                await self.cmd_class._cmd_resolver(*arguments)
            else:
                await self.cmd_class._cmd_resolver("help")

    def text_handler(self, text: str, width: int, option: typing.Literal["center", "left", "right"]) -> str:
        cleaned_text: str = re.sub(pattern=r"\x1B[@-_][0-?]*[ -/]*[@-~]", repl="", string=text)
        padding: int = (width - len(cleaned_text)) // 2
        
        return f"{padding * " "}{text}{padding * " "}" if option == "center" else f"{padding * " "}{text}" if option == "left" else f"{text}{padding * " "}"

connector = Connector()