import sys, argparse, asyncio, aiohttp, json, os, platform
sys.dont_write_bytecode = True
import src.runner as con
from src.core.cmds import Commands

class Main:
    def __init__(self) -> None:
        CONNECTOR.path = os.path.dirname(os.path.realpath(__file__))
        
        with open(f"{CONNECTOR.path}/config.json", "r", encoding="utf-8") as config:
            try:
                self.config: dict[str, dict[str, dict[str, str | bool | list[str] | int]]] = json.load(config)
            except Exception as error:
                raise error
        
        if self.config == {} or not self.config:
            raise ValueError("Config file is empty or doesn't exist.")

        CONNECTOR.c: con.colors.C | con.colors.CNone = con.colors.auto_color_handler()
        CONNECTOR.config = self.config
    
    async def main(self, protocol: str, output_file: str, user_agents: str) -> None:
        c: con.colors.C | con.colors.CNone = CONNECTOR.c
        CONNECTOR.output_file = output_file
        CONNECTOR.protocol = protocol
        print(f"""{c.DRed}
      ________     ________________                    _____             
      ___  __ \\__________  /__  __ \\________________  ____(_)____________
      __  /_/ /  _ \\  __  /__  /_/ /_  ___/  __ \\_  |/_/ / /_  _ \\_  ___/
      _  _, _//  __/ /_/ / _  ____/_  /   / /_/ /_>  <  / //  __/(__  ) 
      /_/ |_| \\___/\\__,_/  /_/     /_/    \\____//_/|_| /_/ \\___//____/  

{CONNECTOR.text_handler(text=f"{c.Red}xRedCrystalx {c.R}| {c.DBlue}2023 {c.R}| {CONNECTOR._version}", width=80, option="center")}
{CONNECTOR.text_handler(text=f"{c.Gray}OS{c.R}: {CONNECTOR.OS} | {c.Gray}Python{c.R}: {platform.python_version()} | {c.Gray}CPU{c.R}: {os.cpu_count()}", width=80, option="center")}
────────────────────────────────────────────────────────────────────────────────""")
        async with aiohttp.ClientSession(headers=CONNECTOR._default_headers) as session:
            CONNECTOR.session = session
            print(f"[{c.Green}+{c.R}] Asynchronous session established: {session.headers.get("User-Agent")}")
            
            await CONNECTOR.cmd_class._scraper_gen(protocol=protocol, config=self.config)
            if not CONNECTOR.proxy_scrapers:
                print(f"[{c.Red}-{c.R}] No website scrapers found. Website scraping is now disabled.")
            else:
                print(f"[{c.Green}+{c.R}] Website scrapers loaded into memory. Scraper count: {len(CONNECTOR.proxy_scrapers)}")
            
            await CONNECTOR.cmd_class.load_user_agents(path=user_agents)
                        
            print(f"────────────────────────────────────────────────────────────────────────────────\n{c.Gray}Use 'help' command for more information.{c.R}")
            try:
                await CONNECTOR.cmd_handler()
            except Exception:
                await CONNECTOR.cmd_class._terminator()

if __name__ == "__main__":
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=52)
    parser = argparse.ArgumentParser(formatter_class=formatter)
    CONNECTOR: con.Connector = con.connector
    CONNECTOR.cmd_class = Commands()
    
    parser.add_argument(
        "-p", "--protocol",
        help="Supported proxy protocols: HTTP, HTTPS (can be lowercased)",
        required=True,
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file name/path default: output.txt",
        default="output.txt",
    )
    parser.add_argument(
        "-ua", "--user-agents",
        help="File/path to user agent's .txt file",
        default=None,
    )
    args: argparse.Namespace = parser.parse_args()
    #print(args)

    if sys.version_info >= (3, 7):
        asyncio.run(Main().main(protocol=args.protocol.lower(), output_file=args.output, user_agents=args.user_agents))
    else:
        print("Please upgrade your python.")

