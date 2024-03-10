# Используем базовый образ Python
FROM python:3.10

# Устанавливаем переменные окружения для Python (для логирования и вывода в консоль)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

SHELL ["/bin/bash", "-c"]




RUN pip install --upgrade pip
RUN apt update

RUN useradd -rms /bin/bash cryptomonkey && chmod 777 /opt /run

# Устанавливаем рабочую директорию контейнера
WORKDIR /cryptomonkey

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /cryptomonkey/

#сменить владельца и скопировать все файлы из текущей директории(где лежит файл Dockerfile) в рабочую(WORKDIR)
#COPY --chown=cryptomonkey:cryptomonkey . .

# Устанавливаем зависимости из requirements.txt
#COPY requirements.txt /app/
RUN pip install -r requirements.txt

USER cryptomonkey

#CMD ["python", "manage.py", "makemirgations"]
CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "CryptoMonkeyWeb.wsgi:application"]