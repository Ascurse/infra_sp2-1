# api_yamdb

**Проект YaMDb собирает отзывы пользователей на произведения. 
Произведения делятся на категории: Книги, Фильмы, Музыка.**

#### Как запустить проект на Docker
##### Запустить проект при скачанном образе api_yamdb последней версии:

`docker run api_yamdb`

##### Создать и активировать виртуальное окружение:

`source venv/bin/activate`

##### Выполнить по очереди команды:

`docker-compose exec web python manage.py migrate`
`docker-compose exec web python manage.py createsuperuser`
`docker-compose exec web python manage.py collectstatic --no-input`