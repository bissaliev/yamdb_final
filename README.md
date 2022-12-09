# yamdb_final
![Django-app workflow](https://github.com/bissaliev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

API YAMDB
API для получения информации и обсуждения наиболее интересных произведений. Для автоматизации развертывания на боевых серверах используется среда виртуализации Docker, а также Docker-compose - инструмент для запуска многоконтейнерных приложений.

Стек технологий:
Python 3
DRF (Django REST framework)
Django ORM
Docker
Gunicorn
nginx
Яндекс Облако(Ubuntu 18.04)
Django 2.2 TLS
PostgreSQL
GIT

О проекте:
Реализована регистрация с кодом подтверждения и дальнейшая авторизация с использованием JWT токена, при отправке запроса к API.

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Документация и возможности API:
К проекту подключен redoc. Для просмотра документации используйте эндпойнт redoc/

## Workflow
* tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
* build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
* deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
* send_message - Отправка уведомления в Telegram

### Подготовка для запуска workflow
Создайте и активируйте виртуальное окружение, обновите pip:
```
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
```
Запустите автотесты:
```
pytest
```
Отредактируйте файл `nginx/default.conf` и в строке `server_name` впишите IP виртуальной машины (сервера).  
Скопируйте подготовленные файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
В репозитории на Гитхабе добавьте данные в `Settings - Secrets - Actions secrets`:
```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)
DB_HOST - db
DB_PORT - 5432
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
```
При внесении любых изменений в проект, после коммита и пуша
```
git add .
git commit -m "..."
git push
```
запускается набор блоков команд jobs (см. файл yamdb_workflow.yaml), т.к. команда `git push` является триггером workflow проекта.
## Как развернуть проект локально:

Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/bissaliev/yamdb_final.git
cd yamdb_final
```
Создайте файл .env командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
В папке проекта создайте образ:
```
docker build -t username/imagename:version api_yamdb/.
```
Соберите контейнеры:
```
docker-compose -f infra/docker-compose.yaml up -d --build
```
или пересоберите:
```
docker-compose up -d --build
```
Выполните миграции:
```
(опционально) docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
Для входа внутрь контейнера используйте команду `exec`:
```
docker-compose exec web sh
```
или
```
docker-compose exec web python manage.py shell
```
или:
```
docker exec -it <container_id> bash
```
Загрузите тестовые данные в БД:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
или
```
docker-compose -f infra/docker-compose.yaml exec web python manage.py loaddata fixtures.json
```


## Как развернуть проект на сервере:
Установите соединение с сервером:
```
ssh username@server_address
```
Проверьте статус nginx:
```
sudo service nginx status
```
Если nginx запущен, остановите его:
```
sudo systemctl stop nginx
```
Установите Docker и Docker-compose:
```
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте корректность установки Docker-compose:
```
sudo  docker-compose --version
```
Создайте папку `nginx`:
```
mkdir nginx
```
### После успешного деплоя:
Соберите статические файлы (статику):
```
docker-compose exec web python manage.py collectstatic --no-input
```
Примените миграции:
```
(опционально) docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
При необходимости наполните базу тестовыми данными из ../yamdb_final/infra/:
```
docker exec -i infra_web_1 python manage.py loaddata --format=json - < fixtures.json
```
или
```
docker-compose exec web python manage.py loaddata fixtures.json
```

Также можно выполнить эти действия внутри контейнера. Отобразите список работающих контейнеров:
```
sudo docker container ls -a
```
В списке контейнеров копируйте CONTAINER ID контейнера username/api_yamdb:latest (username - имя пользователя на DockerHub).   
Выполните вход в контейнер:
```
sudo docker exec -it <CONTAINER_ID> bash
```
Внутри контейнера выполните миграции:
```
python manage.py migrate
```
При необходимости наполните базу данных начальными тестовыми данными:
```
python3 manage.py shell

>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
python manage.py loaddata infra/fixtures.json

## Ссылки
### Документация API YaMDb - эндпойнт:
```json
/redoc/
```
http://158.160.41.34/redoc/
### Развёрнутый проект:
http://158.160.41.34/api/v1/  
http://158.160.41.34/admin/

### Разработчики:

- [@TemaKut](https://github.com/TemaKut)
- [@AnaKuzi](https://github.com/AnaKuzi)
- [@bissaliev](https://github.com/bissaliev)
