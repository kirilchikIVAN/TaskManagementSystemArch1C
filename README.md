# TaskManagementSystemArch1C
TaskManagementSystem project at Arch 1C course


## Project structure

**Ветки:**
1) main - рабочая версия, коммиты только с MR
2) develop - ветка для мерджа в main, коммиты согласовываем
3) developer_name/... ветки разработчиков


**Директории и файлы:**
1) service/ - сервисы (services/UserService.py)
2) db/ - все связанное с базой
3) db/interface/ - взаимодействие с бд (db/intefraces/UserInterface.py
4) StartApp.py - запуск
5) App.py - функционал поддержания жизнедейтельностьи приложения
6) constants.py, settings.py и т.п.