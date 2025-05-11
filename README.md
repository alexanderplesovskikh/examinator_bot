# Бот Тренажёр
Бот Тренажёр помогает студентам готовиться к экзаменам, задавая им вопросы по курсу и анализируя их ответы с помощью
нейросети. Помимо оценки ВЕРНО / НЕВЕРНО он также развёрнуто объясняет оценку и может сообщить правильный ответ.

В данный момент бот умеет задавать вопросы из курса "Компьютерная графика".

## Запуск модели ollama

1. Скачать ollama по ссылке: https://ollama.com/download/
2. Выполнить команду

```bash
ollama pull owl/t-lite
```

3. Проверить, что модель скачалась

```bash
ollama list
```

## Запуск бота

Клонируем репозиторий python-zulip-api

```bash
git clone https://github.com/zulip/python-zulip-api.git
```

Перемещаемся в папку bots

```bash
cd python-zulip-api/zulip_bots/zulip_bots/bots/
```

Здесь содержится несколько ботов, добавим сюда и нашего

```bash
git clone https://gitlab.com/alexandermcme/exerciser.git
```

Перейдём в созданную папку

```bash
mv exerciser exerciser_kg && cd exerciser_kg
```

Создаем файл .env, где прописываем имя пользователя, пароль и ссылку на таблицу для записи ответов в NextCloud. В ссылке на таблицу должно быть два листа "Вопросы и ответы", где будет список вопросов, и "Ответы студентов", куда будут записываться ответы студентов. Структура файла .env:

```
NEXTCLOUD_URL=https://your-server/remote.php/webdav/<folder>/<filename>.xlsx
NEXTCLOUD_USERNAME=username
NEXTCLOUD_PASSWORD=password
```

Ссылка на таблицу: https://drive.miem.tv/index.php/s/BPL7DjSj4CH6d5C

Наконец, запустим бота с помощью скрипта

```bash
./start.sh
```

Этот скрипт:

- Устанавливает зависимости
- Активирует виртуальное окружение
- Поднимает докер с базой данных. В этой базе данных хранятся сообщения, которые нужно отправить или изменить
- Запускает воркер. Он считывает все сообщения в статусе "pending" из БД и отправляет или изменяет их
- Запускает бота Zulip

Чтобы остановить бота, нужно ввести команду:
```bash
./stop.sh
```

## Полезные команды

Посмотреть логи бота в реальном времени
```bash
tail -f zulip_bot.log
```

Посмотреть логи воркера в реальном времени

```bash
tail -f zulip_worker.log
```

Подключиться к базе данных
```bash
docker exec -it exerciser_kg_db psql -U zulip_user zulip_events
```
Теперь в открывшейся строке можно выполнить любой SQL-код, например ```SELECT * FROM events WHERE status = 'pending';```

Остановить:

- Базу данных
    ```bash
    docker compose down
    ```
- Воркер
    ```bash
    pkill -f "python3 worker.py"
    ```
- Бота
    ```bash
    pkill -f "zulip-run-bot exerciser"
    ```
