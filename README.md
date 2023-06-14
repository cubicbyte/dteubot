<div align="center">

<img src="https://user-images.githubusercontent.com/81159301/193612153-e085ffb7-230b-413c-a7b2-c450536cd397.png" alt="Логотип бота" width="200"><br><br>

# Розклад ДТЕУ
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
## [English version](README.md)

Телеграм-бот для зручного перегляду розкладу пар у Державному Торговельно-Економісному Університеті ([ДТЕУ](https://knute.edu.ua)).<br>
Бот доступний для використання: [@dteubot](https://t.me/dteubot).

</div><br>


# Функції

- ✅ Перегляд розкладу пар
- ✅ Перегляд розкладу дзвінків
- ✅ Нагадування про початок пар
- ✅ Інформація про викладачів
- ✅ Перегляд часу до перерви


# Скріншоти

![Скріншот взаємодії](https://github.com/cubicbyte/dteubot/assets/81159301/554f4df6-9812-4a65-b06e-9a6fd47df889)


# Команди

* **/today**<br>
    пари сьогодні
* **/tomorrow**<br>
    пари завтра
* **/left**<br>
    час до кінця/початку пари
* **/calls**<br>
    розклад дзвінків
* **/menu**<br>
    відкрити меню
* **/settings**<br>
    відкрити налаштування
* **/select \<groupId?: `number`\>**<br>
    вибрати групу
* **/lang \<lang?: `[en/uk/ru]`\>**<br>
    вибрати мову

? - необов'язковий параметр
<br><br>



# Запуск
Бота можна запустити двома способами: через Docker та напряму

## 1. Звичайний спосіб

> :warning: Для цього способу вам потрібен **Python** версії **3.8+**

1. Завантажте цей репозиторій та відкрийте в ньому командний рядок.<br>
   Для завантаження, нажміть зелену кнопку **<span style="color: lightgreen;"><> Code</span> > Download ZIP**<br>
   або виконайте команду
   ```shell
   git clone https://github.com/cubicbyte/dteubot
   ```
2. Установіть бібліотеки:
   ```shell
   pip install -r requirements.txt
   ```
3. Створіть та налаштуйте файл `.env` по прикладу `env.example`
4. Запустіть бота наступною командою
   ```shell
   python main.py
   ```

Цей бот також підтримує роботу в іншій директорії: потрібно створити в ній файл .env та виконати команду `python "</шлях/до/папки/з/ботом>/main.py"`<br>
Якщо ж файл не створити, програма буде шукати його в своїй кореневій директорії.

## 2. Docker

> :warning: На даний момент не оновлюється

1. Установіть Docker
2. Створіть директорію, в якій будуть зберігатися дані бота
3. В цій директорії створіть файл `.env` та заповніть його за прикладом файла [env.example](env.example)
4. Виконайте наступну команду:
    - Для Windows:
        ```shell
        docker run -d -v ${PWD}:/data --name schedule-bot angron42/sute-schedule-bot
        ```
    - Для Linux:
        ```shell
        docker run -d -v $(pwd):/data --name schedule-bot angron42/sute-schedule-bot
        ```

Щоб зупинити, виконайте команду
```shell
docker stop schedule-bot
```


> **Note** *Ви також можете налаштувати цього бота для відображення розкладу інших університетів, що використовують систему АСУ МКР.*<br>
