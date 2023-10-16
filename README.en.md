<div align="center">

<img src="https://user-images.githubusercontent.com/81159301/193612153-e085ffb7-230b-413c-a7b2-c450536cd397.png" alt="Логотип бота" width="200"><br><br>

# Розклад ДТЕУ
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
## [English version](README.en.md)

Telegram bot for getting the schedule in Ukrainian State University of Trade and Economics ([SUTE](https://knute.edu.ua)).<br>
You can try the bot live: [@dteubot](https://t.me/dteubot).

</div><br>


# Features

- ✅ View the classes schedule
- ✅ Reminders about classes
- ✅ Link to teacher's profile
- ✅ Stable work even when the site is unavailable
- And other features, such as viewing the bell schedule, list of students in the group and time to break.

# Screenshots

![Screenshot of usage](https://github.com/cubicbyte/dteubot/assets/81159301/554f4df6-9812-4a65-b06e-9a6fd47df889)


# Commands

* **/today**<br>
  lessons today
* **/tomorrow**<br>
  lessons tomorrow
* **/left**<br>
  time until the end/start of the lesson
* **/calls**<br>
  calls schedule
* **/settings**<br>
  open settings
* **/group \<groupId?: `number`\>**<br>
  select group
* **/lang \<lang?: `[en/uk/ru]`\>**<br>
  select language

? - optional parameter
<br><br>


# Startup

Bot can be started in three ways:
- Using executable file (.exe for Windows)
- Using Docker container
- Using manual compilation

## 1. Normal way

Bot needs a database [PostgreSQL](https://www.postgresql.org/download/) to work.

### 1. Database setup

You need to create a database and configure it using the [setup.sql](sql/setup.sql) file.

1. Download and install PostgreSQL
2. Create a database and setup it using [setup.sql](sql/setup.sql) file

### 2. Bot setup

1. Download [latest bot version](https://github.com/cubicbyte/dteubot/releases/latest)
2. Put file `dteubot` in any directory you want to store bot data
3. Run the file with this command: (after first run, config file will be created)
   ```shell
   ./dteubot
   ```
4. Open `.env` file and fill all required fields, such as bot token and database connection parameters.

### 3. Bot launch

1. Run the file with this command:
   ```shell
   ./dteubot
   ```

Done! Now you can use the bot.

## 2. Docker

At the moment in development.

## 3. Manual compilation

> :warning: For this method you need **Go** version **1.21+** - [download](https://golang.org/dl/)

1. Download this repository and open command line in it.<br>
   To download, click the green button **<span style="color: lightgreen;"><> Code</span> > Download ZIP**<br>
   or execute command
   ```shell
   git clone https://github.com/cubicbyte/dteubot
   ```
2. Make sure you have **Go** compiler installed and run command
   ```shell
   go build
   ```

Now you have executable file `dteubot`. Go to section **1. Normal way**
