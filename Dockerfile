FROM docker.io/python:3.12.7

# PYTHONDONTWRITEBYTECODE=1 - не создавать файлы кэша .pyc
# PYTHONUNBUFFERED=1 - отключить буферизацию вывода
# DEBIAN_FRONTEND=noninteractive - устанавливать утилиты без интерактива (-y, e.t.c...)
ENV HOME=/home/dude \
    PROJECT_DIR=/home/dude/planning \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

RUN mkdir -p $PROJECT_DIR \
    && groupadd -r dude \
    && useradd -r -g dude dude \
    && apt-get update && apt-get upgrade -y && apt-get autoremove -y \
    && apt-get install curl \
    && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt $PROJECT_DIR
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ./$PROJECT_DIR/requirements.txt

COPY src $PROJECT_DIR/src
COPY planning_entrypoint.sh $PROJECT_DIR
RUN chmod +x $PROJECT_DIR/planning_entrypoint.sh

WORKDIR $PROJECT_DIR/src
RUN chown -R dude:dude $HOME
USER dude
EXPOSE 8000

# указываем скрипт как точку входа
ENTRYPOINT ["/home/dude/planning/planning_entrypoint.sh"]
