0. Установка зависимостей и создание директории

sudo apt install python3.12-venv;
sudo apt install python3-pip;

mkdir backend
cd backend
python3 -m venv venv
source venv/bin/activate

### установка докер
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

1. Создаём проект Django + DRF

# Устанавливаем зависимости:
pip install django djangorestframework psycopg2-binary

# Создаём проект:
django-admin startproject config .

# Создаём приложение:
python manage.py startapp api

2. Добавляем DRF в settings

config/settings.py:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'api',
]


3. Простой пример API

config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

api/views.py:

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello DRF"})


api/urls.py:

from django.urls import path
from .views import hello

urlpatterns = [
    path('hello/', hello),
]


http://192.168.1.178:8000/


4. Подключаем PostgreSQL

В config/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app',
        'USER': 'app',
        'PASSWORD': 'secret',
        'HOST': 'db',
        'PORT': 5432,
    }
}


5. requirements.txt
pip freeze > requirements.txt


6. Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


7. docker-compose.yml
version: "3.9"

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_NAME=app
      - DB_USER=app
      - DB_PASSWORD=secret
      - DB_HOST=db
# CREATE DATABASE mydb;
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:



8. Запуск
docker compose up --build -d
для работы в фоне нужно добавит аргумент -d

9. Миграции

В другом терминале:

docker compose exec backend python manage.py migrate



Создать админа:

docker compose exec backend python manage.py createsuperuser



10. Проверка

API:
http://localhost:8000/api/hello/

Admin:
http://localhost:8000/admin/


Добавить хост в allowed hosts

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')






# DOcker


### установка докер
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

### сборка
sudo docker build -t my-nextjs-app .

### запуск контейнера
docker run -d \
  --name frontend \
  -p 3000:3000 \
  my-nextjs-app

### список образов
sudo docker images

# список контейнеров
sudo docker ps -a

# логи
sudo docker logs frontend

### убить все контейнеры
sudo docker stop $(docker ps -q); sudo docker rm $(docker ps -aq);



sudo docker compose exec backend python manage.pywget http://127.0.0.1:8000/ runserver 0.0.0.0:8000