# Bcrypto bot!
[![N|Solid](https://bombcrypto.io/wp-content/uploads/2021/08/12.png)](https://nodesource.com/products/nsolid)
## A bot that automates farming at bomb crypto NFT game




This is the docs of python bcrypto bot.


## Features

- Multiaccount
- Smart farming
- Discord integration
- Error handlers and fallbacks

## Tech

Dillinger uses a number of open source projects to work properly:

- [Python]
- [pyautogui] - Manage keyboard and mouse to automate tasks
- [pysimplegui] - Create user interface
- [opencv-python] - Compare screen with references
- [cx-freeze] - Generate bot executable

## Requirements

Python 3+ is required to run the script. If you want to test or make changes to bot scripts you'll need to complete the following installation steps. In case you just want to use bot, look for executable version and ignore installation steps.


## Installation

Bcrypto bot uses a virtual environment to wrap dependencies and to make easier to run regardless of ambient (obviously respecting OS particularities)

Create virtual environment:

```sh
python -m venv environment
```

Activate virtual environment:
OSX / LINUX
```sh
source environment/bin/activate
```
WINDOWS
```sh
environment/Scripts/activate.bat
```

Now you should se your environment specified at the beginning of your cmd line. Like this: 
```sh
(environment) olivera@Macbook bcrypto-bot:
```

Now lets install our requirements, with the following command you are going to install all requirements the script needs to run properly, they are previously listed inside requirements.txt file:

```sh
pip install -r requirements.txt
or
python pip install -r requirements.txt
```

## Generating executable
Platform: WINDOWS
setup.py is already configured to generate windows build, so all you need to do is run the following command:
```sh
python setup.py build
```
you will also need to copy "assets", "configs.txt" and ".env" into generated build folder, same folder that executable is located

Platform: OS and Linux
```sh
soon!!
```


## Development

Want to contribute? Great!
Found an issue or bug? Let me know!

Feedbacks are always very welcome.


## License

**This was not suposed to be free, but if you're being able to see it, enjoy while you can**

