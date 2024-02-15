import sys, typing, asyncio, json, random
sys.dont_write_bytecode = True
from src.runner import connector, IPv6p, IPv4p
import src.core.websiteScraper as wScraper
import src.core.proxyTester as pTester

class Commands:
    def __init__(self) -> None:
        self.commands: dict[str, dict | typing.Callable] = {
            ("load", "add", "upload") : {
                ("user_agents", "agents", "user-agents") : self.load_user_agents,
                ("proxy_servers", "proxies", "IPs") : self.load_proxy_IP_addresses
            }, 
            ("scan", "scrape") : {
                ("website", "websites", "sites", "site", "links") : self.website_scraper
                
            },
            ("reload") : {
                ("config", "config_file", "configuration", "configuration_file", "cfg") : self.reload_config
            },
            ("check", "verify", "test") : self.proxy_tester,
            ("help", "h") :  self.help,
            ("exit", "kill", "end", "quit", "stop", "terminate") : self._terminator
        }
    
    async def _cmd_resolver(self, *args) -> None:
        async def recursive(index: int, path: str | dict) -> None:
            for key in path.keys():
                if args[index].lower() in key:
                    if isinstance(path[key], dict):
                        try:
                            await recursive(index=index+1, path=path[key])
                        except Exception:
                            await self.help(cmd="help")
                    else:
                        await path[key](*args[index+1:])

        await recursive(index=0, path=self.commands)
    
    def _read_file(self, path: str, *ARG) -> str | bytes | bool:
        if path:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    return file.read()
            except Exception:
                try:
                    with open(f"{connector.path}/{path}", "r", encoding="utf-8") as file:
                        return file.read()
                except Exception:
                    return False
        return False
    
    def _save_file(self, path: str, data: str | bytes, *ARG) -> None:
        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(data)
                    return True
            except Exception:
                try:
                    with open(f"{connector.path}/{path}", "w", encoding="utf-8") as file:
                        file.write(data)
                        return True
                except Exception:
                    return False
        return False

    async def _scraper_gen(self, protocol: str, config: dict[str, dict[str | typing.Any]], *ARG) -> None:
        def recursive_gen(link: str, data: dict[str, typing.Any], index: int, db: dict[str, typing.Any]) -> None:
            for key, value in list(data.items())[index:]:
                if key.isupper() is False:
                    if isinstance(value, list):
                        for v in value:
                            db[key] = v
                            recursive_gen(link=link, data=data, index=index+1, db=db)
                        break
                    else:
                        db[key] = value
                        index += 1
                else:
                    index += 1
            else:
                match data["SCRAPER"]:
                    case "scraper":
                        connector.proxy_scrapers.append(wScraper.Scraper(url=link.format(**db), protocol=protocol, session=connector.session))
                    case "table":
                        connector.proxy_scrapers.append(wScraper.TableScraper(url=link.format(**db), protocol=protocol, session=connector.session))
                    case "json":
                        connector.proxy_scrapers.append(wScraper.JSONScraper(url=link.format(**db), protocol=protocol, session=connector.session))
                    #if something random, throw the basic scraper
                    case _:
                        connector.proxy_scrapers.append(wScraper.Scraper(url=link.format(**db), protocol=protocol, session=connector.session))

        for link, data in config["WebsiteScraper"].items():
            if not data.get("SCRAPER"):
                print(f"Ignoring {link}. --- no scraper specified!")
                continue
            
            if protocol in data["TYPE"]:
                recursive_gen(link=link, data=data, index=0, db={"type": protocol})

    async def _terminator(self) -> None:
        await connector.session.close()
        sys.exit(0)


    async def load_user_agents(self, path: str, *ARG) -> None:
        data: str | bytes | bool = self._read_file(path=path)
        
        if path:
            if data:
                try:
                    connector.user_agents = data.splitlines()
                    print(f"[{connector.c.Green}+{connector.c.R}] User agents loaded into memory. Agents count: {len(connector.user_agents)}")
                except Exception:
                    print(f"[{connector.c.Red}-{connector.c.R}] Failed to load user agents from file. Default user agent will be used.")
            else:
                print(f"[{connector.c.Red}-{connector.c.R}] Failed to load user agents from file. Default user agent will be used.")
        else:
            print(f"[{connector.c.Yellow}!{connector.c.R}] No user agents file was provided. Default user agent will be used.")
            
    async def load_proxy_IP_addresses(self, path: str, *ARG) -> None:
        data: str | bytes | bool = self._read_file(path=path)
        
        if path:
            if data:
                try:
                    connector.proxies = [IP for IP in data.splitlines() if IPv4p.search(string=IP) or IPv6p.search(string=IP)]
                    print(f"[{connector.c.Green}+{connector.c.R}] Proxy IP addresses loaded into memory. Proxies count: {len(connector.proxies)}")
                except Exception:
                    print(f"[{connector.c.Red}-{connector.c.R}] Failed to load proxy IP addresses from file.")
            else:
                print(f"[{connector.c.Red}-{connector.c.R}] Failed to load proxy IP addresses from file.")
        else:
            print(f"[{connector.c.Yellow}!{connector.c.R}] No user proxy IP file was provided.")  
    
    async def reload_config(self) -> None:
        data: str | bytes | bool = self._read_file(path="config.json")
        if data:
            connector.config = json.loads(data)
            print(f"[{connector.c.Green}+{connector.c.R}] Config.json successfully reloaded. New data has been added to the memory.")
        else:
            print(f"[{connector.c.Red}-{connector.c.R}] Failed to reload config.json. No changes were applied.")
        return
    
    
    async def website_scraper(self, *ARG) -> None:
        async def start_scraper(scraper: wScraper.Scraper | wScraper.TableScraper | wScraper.JSONScraper) -> None:
            try:
                connector.proxies.extend(await scraper.scrape())
            except Exception:
                pass
        
        connector.proxies = []
        async with asyncio.TaskGroup() as group:
            [group.create_task(start_scraper(scraper=scraper)) for scraper in connector.proxy_scrapers]
        
        self._save_file(path=connector.output_file, data="\n".join(connector.proxies))

    async def proxy_tester(self, agent: str = "", *ARG) -> None:
        if connector.protocol == "http":
            funcs: list[pTester.HTTPtester] = [pTester.HTTPtester(protocol=connector.protocol, proxy=IP, user_agent=connector._default_user_agent if agent not in ("--random-user-agent", "-rua") else (random.choice(connector.user_agents if connector.user_agents else [connector._default_user_agent]))) for IP in connector.proxies]
        
        if funcs:
            async with asyncio.TaskGroup() as group:
                tasks: list[asyncio.Task] = [group.create_task(fun.check(timeout=connector.config["Configuration"]["testerTimeout"])) for fun in funcs]
            
    async def help(self, cmd: str = "", *ARG) -> None:
        _default: str = "Help page: {cmd}\n\nDefault: {default}\nAliases: {aliases}\nDescription: {description}\n\n" 
        if cmd in ("load",):
            print(f"{_default.format(cmd=cmd, default="load", aliases="add, upload", description="Load data into the memory")}\
Options:\n\
- proxies [PROXY FILE]  > Loads proxy server IPs into the memory. Aliases: IPs, proxy_servers\n\
- agents [AGENT FILE]   > Loads user agents into the memory. Aliases: user_agents, user-agents")
        elif cmd in ("scan", "scrape"):
            print(f"{_default.format(cmd=cmd, default="scrape", aliases="scan", description="Scrape for proxy servers.")}\
Options:\n\
- websites [OPTIONAL: --random-user-agent | -rua]  > Scrapes websites from the config. Aliases: website")

        elif cmd in ("reload",):
            print(f"{_default.format(cmd=cmd, default="reload", aliases="/", description="Reloads specified option and saves it in the memory.")}\
Options:\n\
- config [NONE] > Reloads config file. Aliases: cfg, config_file, configuration, configuration_file")

        elif cmd in ("exit", "kill", "end", "quit", "stop", "terminate"):
            print(f"{_default.format(cmd=cmd, default="exit", aliases="kill, end, quit, stop, terminate", description="Terminates RedProxies processes.")}")
        
        else:
            print(f"{_default.format(cmd=cmd, default="help", aliases="h", description="Shows help menu of specific option.")}\
Options:\n\
- load    > Displays options for load command and its aliases.\n\
- reload  > Displays options for reload command and its aliases.\n\
- scrape  > Displays options for scrape command and its aliases.\n\
- exit    > Displays options for exit command and its aliases.")