[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/+jJhUfsfFCn4zZDk0)      [![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/major/start?startapp=339631649)

![demo](https://github.com/user-attachments/assets/94ab0cfd-07d2-449d-ae41-1a1807402e3e)



## Recommendation before use

# 🔥🔥 PYTHON version must be 3.10 🔥🔥

> 🇷 🇺 README in russian available [here](README-RU.md)

## Features  
|                         Feature                          | Supported |
|:--------------------------------------------------------:|:---------:|
|                      Multithreading                      |     ✅     |
|                 Proxy binding to session                 |     ✅     |
|                      Auto Referral                       |     ✅     |
|                    Auto Claim Task                       |     ✅     |
|                     Auto Roulette                        |     ✅     |
|                  Auto Daily Streak                       |     ✅     |
|              Support for telethon .session               |     ✅     |


## [Settings](https://github.com/GravelFire/MajorBot/blob/main/.env-example/)
|        Settings         |                                      Description                                       |
|:-----------------------:|:--------------------------------------------------------------------------------------:|
|  **API_ID / API_HASH**  |        Platform data from which to run the Telegram session (default - android)        |
| **TASKS_WITH_JOIN_CHANNEL** | Whether to perform tasks with joining channels (True / False)                  |
|    **HOLD_COIN**        |                         Ammount coins in Hold Coin (e.g. [585, 600])             |
|    **SWIPE_COIN**       |                         Ammount coins in Swipe Coin (e.g. [2000, 3000])          |
| **REF_ID**           |                   Your referral id after startapp= (Your telegram ID)                  |
| **USE_RANDOM_DELAY_IN_RUN**  | Whether to use random delay at startup (True / False)                                               |
| **RANDOM_DELAY_IN_RUN**      | Random delay at startup (e.g. [0, 15])                                                              |
| **FAKE_USER AGENT** |                   Use a fake user agent for sessions (True / False)                    |
| **SLEEP_TIME**          |                   Delay before the next lap (e.g. [1800, 3600])                         |
| **USE_PROXY_FROM_FILE** |      Whether to use a proxy from the `bot/config/proxies.txt` file (True / False)      |

## Quick Start 📚

To fast install libraries and run bot - open run.bat on Windows or run.sh on Linux

## Prerequisites
Before you begin, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) **version 3.10**

## Obtaining API Keys
1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the API_ID and API_HASH provided after registering your application in the .env file.

## Installation
You can download the [**repository**](https://github.com/GravelFire/MajorBot) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/GravelFire/MajorBot.git
cd MajorBot
```

Then you can do automatic installation by typing:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

You can also use arguments for quick start, for example:
```shell
~/MajorBot >>> python3 main.py --action (1/2)
# Or
~/MajorBot >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```

You can also use arguments for quick start, for example:
```shell
~/MajorBot >>> python main.py --action (1/2)
# Or
~/MajorBot >>> python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```
