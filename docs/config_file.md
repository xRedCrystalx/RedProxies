# CONFIGURATION FILE
This project is made to be as customizable as possible which is why I have created a config file. Currently, this is a **JSON** file, but it may be changed to **YAML** or other file types in future. Configuration file can be found [here](https://github.com/xRedCrystalx/RedProxies/blob/main/config.json).

## General Config:
General config can be found under the `Configuration` key.
The following options are available:
- **testerDefaultWebsiteHTTPS:** website used for HTTPS proxy testing *(default: https://www.google.com)*
- **testerDefaultWebsiteHTTP:** website used for HTTP proxy testing  *(default: http://neverssl.com)*
- **testerTimeout:**  timeout in seconds when waiting for a response from the server *(default: 10)*

## Scraper Config:
Scraper config can be found under the `WebsiteScraper` key.
```json
{
    "<link with placeholders eg. https://test.com/smt.php?test={abc}>" : {
        "SCRAPER" : str
        "TYPE" : list, str

        "<custom lowercased variable eg. abc>" : str, bool, list, int, float
    },
}
```
Each of the scraping `link` requires:
- **SCRAPER** - *must be fully UPPERCASED*; only allowed to be one of: **["scraper", "json", "table"]** 

      specifies scraper that will be used for that link
- **TYPE** - *must be fully UPPERCASED*; can be string or list of: **["http", "https", "socks4", "socks5"]** 

      specifies which types of proxies that website offers
- **custom value** - *must be fully lowercased*; optional

Custom values:
- **KEY** -  **str** - *must be fully lowercased*
  
      will be used as placeholder of the link arguments (look at the example)
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