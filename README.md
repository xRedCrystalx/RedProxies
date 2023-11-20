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
usage: main.py [-h] -p ARG [-o ARG]

options:
  -h, --help            show this help message and exit
  -p ARG, --proxy ARG   Supported proxy type: HTTP, HTTPS (can be lowercased)
  -o ARG, --output ARG  Output file name to save .txt file
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
