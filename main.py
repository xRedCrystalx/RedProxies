import sys, argparse, asyncio, aiohttp, json, os, typing, random
sys.dont_write_bytecode = True
from src.scraper import IPAddress, Scraper, TableScraper

class Main:
    def __init__(self) -> None:
        print("Initializing..")
        self.proxies: list[IPAddress] = []
        self.proxy_scrapers: list[Scraper | TableScraper] = []
        self.path: str = os.path.dirname(os.path.realpath(__file__))
        self.session: aiohttp.ClientSession = None
        
        with open(f"{self.path}/config.json", "r", encoding="utf-8") as config:
            try:
                self.config: dict[str, dict[str, str | bool | list[str] | int]] = json.load(config)
            except Exception as error:
                raise error

    def scraper_gen(self, method: str, config: dict[str, dict[str | typing.Any]]) -> None:
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
                match data["SCRAPER"]:
                    case "table":
                        self.proxy_scrapers.append(TableScraper(url=link.format(**db), session=self.session))
                    case "scraper":
                        self.proxy_scrapers.append(Scraper(url=link.format(**db), session=self.session))
                    #if something random, throw the basic scraper
                    case _:
                        self.proxy_scrapers.append(Scraper(url=link.format(**db), session=self.session))

        for link, data in config.items():
            if not data.get("SCRAPER"):
                print(f"Ignoring {link}. --- no scraper specified!")
                continue
            
            if method in data["TYPE"]:
                db: dict[str, str | int | bool] = {"type": method}
                for i, (key, value) in enumerate(data.items()):
                    if key.isupper() is False:
                        if isinstance(value, list):
                            for v in value:
                                db[key] = v
                                recursive_gen(link=link, data=data, index=i+1, db=db)
                            break
                        else:
                            db[key] = value
                else:
                    match data["SCRAPER"]:
                        case "table":
                            self.proxy_scrapers.append(TableScraper(url=link.format(**db), session=self.session))
                        case "scraper":
                            self.proxy_scrapers.append(Scraper(url=link.format(**db), session=self.session))
                        #if something random, throw the basic scraper
                        case _:
                            self.proxy_scrapers.append(Scraper(url=link.format(**db), session=self.session))
    
    async def main(self, method: str, output_file: str) -> None:
        async def start_scraper(scraper: Scraper | TableScraper) -> None:
            try:
                self.proxies.extend(await scraper.scrape())
            except Exception:
                pass    
        
        if self.config == {} or not self.config:
            raise ValueError("Config file is empty or doesn't exist.")
        
        async with aiohttp.ClientSession() as session:
            print("--- Session Started ---")
            self.session = session
            self.scraper_gen(method=method, config=self.config)

            async with asyncio.TaskGroup() as group:
                [group.create_task(start_scraper(scraper=scraper)) for scraper in self.proxy_scrapers]
        print("--- Session Closed ---")
        
        try:
            with open(output_file, "w") as f:
                f.write("\n".join([repr(IP) for IP in self.proxies]))
            print(f"Successfully saved proxy IPs in text file. {output_file}")
        except Exception as error:
            print(f"Failed to save proxy IPs. {type(error).__name__}: {error}")

        print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--proxy",
        help="Supported proxy type: HTTP, HTTPS (can be lowercased)",
        required=True,
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file name to save .txt file",
        default="output.txt",
    )
    args: argparse.Namespace = parser.parse_args()

    if sys.version_info >= (3, 7):
        asyncio.run(Main().main(args.proxy.lower(), args.output))
    else:
        print("Please upgrade your python.")