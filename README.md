# RedProxies
RedProxies is a python tool that helps with scraping, verifying and using (in future) proxy servers that are open and accessible by anyone.

Please note that this project is still under development and I have plans to add many more features including **SOCKS proxy support**, **proxy tunneling** and other custom features. Feel free to report all the bugs and ideas in [issues](https://github.com/xRedCrystalx/RedProxies/issues). Thanks!

## Instalation
**Windows/Linux/MacOS** - *requires qit to be installed*
```
git clone https://github.com/xRedCrystalx/RedProxies.git
cd RedProxies/
```
Make sure to have **Python 3.12** and **PIP** installed.
```
pip install -r requirements.txt
```
*It is recommended to run project in virtual environment (venv)*
```java
python3 -m venv .venv

source .venv/bin/activate    // bash - Linux
.venv\Scripts\Activate.ps1   // powershell - Windows
```

## Usage

```c
usage: main.py [-h] -p PROXY [-o OUTPUT]

options:
  -h, --help                   Show this help message and exit
  -p PROXY, --proxy PROXY      Supported proxy type: HTTP, HTTPS (can be lowercased)
  -o OUTPUT, --output OUTPUT   Output file name to save .txt file

```
**Usage Examples**
```
python3 main.py -p HTTP -o proxy_ips.txt

python3 main.py --proxy HTTPS
```
## Configuration:
Project is made to be as customizable as possible, that is why I have created a config file. Currently, this is **JSON** file, but it could get changed to **YAML** or other file types in future.
```json
{
    "<link>" : {
        "SCRAPER" : str
        "TYPE" : list, str

        "<custom lowercased variable>" : str, bool, list, int, float
    },
}
```
Each of the scraping `link` requires:
- **SCRAPER** - *must be fully UPPERCASED*; only allowed to be one of: **["scraper", "json", "table"]** 

      specifies scraper that will be used for that link
- **TYPE** - *must be fully UPPERCASED*; can be string or list of: **["http", "https", "socks4", "socks5"]** 

      specifies which types of proxies that link has
- **custom value** - *must be fully lowercased*; optional

Custom values:
- **KEY** -  **str** - *must be fully lowercased*
  
      will be used as placeholder of the link (look at the example)
- **VALUE** - **str, bool, int, float, list**
  
      will be used as value of placeholders, lists will be iterated by the program.

**Example:**
```json
{
    "https://api.proxyscrape.com/?request=getproxies&proxytype={type}&timeout={timeout}&country={country}" : {
        "SCRAPER" : "scraper",
        "TYPE" : ["https", "http"],
        "timeout" : 1000,
        "country" : "All"
    }
}
```

## License
This software is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/legalcode)

You can find this project's licence [here](https://github.com/xRedCrystalx/RedProxies/blob/main/LICENSE).
