<div align="center">
<img src="https://user-images.githubusercontent.com/81159301/193612153-e085ffb7-230b-413c-a7b2-c450536cd397.png" alt="Logo" width="200"><br><br>

# SUTE Schedule Bot
[![Python 3.6+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Telegram bot for getting the schedule in Ukrainian State University of Trade and Economics ([SUTE](https://knute.edu.ua)).<br>
You can try the bot live: ([@dteubot](https://t.me/dteubot))
</div>

> **Note** You can also configure this bot to display schedule from other universities using the MKR ACS system



# Screenshots
![Bot screenshot](https://user-images.githubusercontent.com/81159301/193561985-2414eafb-3423-4ef6-b149-24926831df7a.png)



# Commands
Basically, the main way to control the bot - with the buttons. But the bot also supports the following commands:
* **/today**<br>
    lessons today
* **/tomorrow**<br>
    lessons tomorrow
* **/left**<br>
    time until the end/start of the lesson
* **/calls**<br>
    calls schedule
* **/menu**<br>
    open menu
* **/settings**<br>
    open settings
* **/select \<groupId?: `number`\>**<br>
    select group
* **/lang \<lang?: `[en/uk/ru]`\>**<br>
    select language

? - optional parameter
<br><br>



# Startup
The bot can be started in two ways: Docker and directly

## 1. The usual way

> :warning: For this method you need **Python** version **3.7+**

1. Download this repository and open a command line in it.<br>
   To download, click the green button **<span style="color: lightgreen;"><> Code</span> > Download ZIP**<br>
   or execute the command
   ```shell
   git clone https://github.com/cubicbyte/dteubot
   ```
2. Install the libraries:
    ```shell
    pip install -r requirements.txt
    ```
3. Configure the file `.env` by example `env.example`
4. Start the bot with the following comand
    ```shell
    python main.py
    ```

This bot also supports running in another directory: you need to create an .env file in it and execute the command `python "</path/to/bot/folder>/main.py"`<br>
If the file is not created, the program will search for it in its root directory.

## 2. Docker
1. Install Docker
2. Create a directory in which the bot data will be stored
3. In this directory, create an `.env` file by example [env.example](env.example)
4. Run the following command:
    - For Windows:
        ```shell
        docker run -d -v ${PWD}:/data --name schedule-bot angron42/sute-schedule-bot
        ```
    - For Linux:
        ```shell
        docker run -d -v $(pwd):/data --name schedule-bot angron42/sute-schedule-bot
        ```

To stop, execute the command
```shell
docker stop schedule-bot
```

