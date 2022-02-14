## Учебный проект 15 спринта факультета бэкенд-разработки 
**Проект YaMDb собирает отзывы пользователей на произведения.**

**Произведения делятся на категории: Книги, Фильмы, Музыка.**

## Переменные окружения:
- Python==3.7
- Django==2.2.6
- django-filter==2.4.0
- django-rest-authtoken==2.1.3
- djangorestframework==3.12.4
- djangorestframework-simplejwt==4.7.2
- Docker==20.10.12
- Nginx==1.21.3-alpine
- attrs==21.2.0
- certifi==2021.5.30
- chardet==4.0.0
- Django==2.2.6
- django-filter==2.4.0
- django-rest-authtoken==2.1.3
- djangorestframework==3.12.4
- djangorestframework-simplejwt==4.7.2
- idna==2.10
- importlib-metadata==4.6.1
- iniconfig==1.1.1
- numpy==1.21.0
- packaging==21.0
- pluggy==0.13.1
- py==1.10.0
- PyJWT==2.1.0
- pyparsing==2.4.7
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- pytz==2021.1
- requests==2.25.1
- simplejwt==2.0.1
- sqlparse==0.4.1
- toml==0.10.2
- typing==3.7.4.3
- typing-extensions==3.10.0.0
- urllib3==1.26.6
- zipp==3.5.0
- gunicorn==20.0.4
- psycopg2-binary==2.8.6

## Руководство по установке Docker
Информация по установке Docker  [здесь](https://docs.docker.com/engine/install/)

## Руководство по запуску проекта:

Клонировать репозиторий:

```bash
git clone https://github.com/Tar8117/infra_sp2.git
```
Либо, если используете доступ к Github через SSH:
```bash
git clone git@github.com:Tar8117/infra_sp2.git
```
Перейти в склонированный репозиторий:
```bash
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

```bash
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Запустить приложение в контейнерах:

*из директории `infra/`*
```bash
docker-compose up -d --build
```

Выполнить миграции:

*из директории `infra/`*
```bash
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

*из директории `infra/`*
```bash
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

*из директории `infra/`*
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Остановить приложение в контейнерах:

*из директории `infra/`*
```bash
docker-compose down -v
```
Запуск `pytest`:

*при запущенном виртуальном окружении*
```bash
cd infra_sp2 && pytest
```

### Документация API с примерами:

```json
/redoc/
```

### Шаблон наполнения env-файла
см.
```bash
infra/.env.template
```

### описание команды для заполнения базы данными
```bash
cd api_yamdb && python manage.py loaddata ../infra/fixtures.json
```
