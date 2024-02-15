# RedProxies
RedProxies is a python tool that helps with scraping, verifying and using (in the future) proxy servers that are open and accessible by anyone.

Please note that this project is still under development and I have plans to add many more features including **SOCKS proxy support**, **proxy tunneling** and other custom features. Feel free to report all the bugs and ideas in [issues](https://github.com/xRedCrystalx/RedProxies/issues). Thanks!

## Installation
**Windows/Linux/MacOS** - *requires qit to be installed*
```
git clone https://github.com/xRedCrystalx/RedProxies.git
cd RedProxies/
```
Make sure to have **Python 3.12** and **PIP** installed.
```
pip install -r requirements.txt
```
*It is recommended to run the project in a virtual environment (venv)*
```java
python3 -m venv .venv

source .venv/bin/activate    // bash - Linux
.venv\Scripts\Activate.ps1   // powershell - Windows
```

## Usage
```c
usage: main.py [-h] -p PROTOCOL [-o OUTPUT] [-ua USER_AGENTS]

options:
  -h, --help                                  show this help message and exit
  -p PROTOCOL, --protocol PROTOCOL            Supported proxy protocols: HTTP, HTTPS (can be lowercased)
  -o OUTPUT, --output OUTPUT                  Output file name/path default: output.txt
  -ua USER_AGENTS, --user-agents USER_AGENTS  File/path to user agent's .txt file
```
**Usage Examples**
```
python3 main.py -p HTTP -o proxy_ips.txt

python3 main.py --proxy HTTPS
```

## Documentation
All documentation can be found [here](https://github.com/xRedCrystalx/RedProxies/tree/main/docs).

- [Configuration File](https://github.com/xRedCrystalx/RedProxies/blob/main/docs/config_file.md)

## License
This software is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/legalcode)

You can find this project's licence [here](https://github.com/xRedCrystalx/RedProxies/blob/main/LICENSE).


## Disclaimer:

The RedProxies tool is provided for educational and informational purposes only. The creators and contributors of this tool do not condone or support any illegal or unethical activities, including but not limited to unauthorized access to computer systems or networks.

By using the RedProxies, you agree to use it responsibly and in compliance with all applicable laws and regulations. You acknowledge that the tool may be used to scan networks and systems and gaining access to them, but you are solely responsible for obtaining proper authorization before conducting any scanning activities.

The creators and contributors of this tool shall not be held responsible or liable for any misuse, damage, or consequences resulting from the use of the tool by third parties. Users of the tool assume all risks associated with its use and agree to indemnify and hold harmless the creators and contributors from any claims, damages, or losses arising from such use.

Furthermore, the RedProxies is provided "as is" without any warranty or guarantee of its accuracy, reliability, or suitability for any particular purpose. The creators and contributors make no representations or warranties regarding the performance or effectiveness of the tool.

By using the RedProxies, you acknowledge and accept these terms and conditions. If you do not agree with these terms, you should not use the tool.
