<div align="center">
<img src="https://user-images.githubusercontent.com/81159301/193612153-e085ffb7-230b-413c-a7b2-c450536cd397.png" alt="Logo" width="200"><br><br>

# SUTE Schedule Bot

[![Python 3.6+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Bot for getting the schedule in [SUTE](https://mia1.knute.edu.ua).<br>
*\*You can also configure this bot to display schedule from other universities using the MKR ACS system\**<br>
You can try the bot live ([link](https://t.me/dteubot))<br>

</div>

# Screenshots
![Bot screenshot](https://user-images.githubusercontent.com/81159301/193561985-2414eafb-3423-4ef6-b149-24926831df7a.png)

# Commands

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

# Setup

1. Run `pip install -r requirements.txt`
2. Setup file `.env` using `.env.example` as an example
3. Launch. `python ./sute-schedule-bot`

This bot also supports running in another directory, you just need to create an .env file in it.<br>
If not created, the bot will use the .env file from its root directory

