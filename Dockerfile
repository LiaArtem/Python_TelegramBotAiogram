FROM python:latest

# set work directory
WORKDIR /usr/src/app/

RUN mkdir -p /usr/src/app/service/
RUN mkdir -p /usr/src/app/handlers/
RUN mkdir -p /usr/src/app/database/
RUN mkdir -p /usr/src/app/others/
RUN mkdir -p /usr/src/app/log/

# copy project
COPY ./*.py /usr/src/app/
COPY ./service/*.py /usr/src/app/service/
COPY ./handlers/*.py /usr/src/app/handlers/
COPY ./others/*.py /usr/src/app/others/
COPY ./settings_docker /usr/src/app/settings


# install dependencies
RUN pip install aiogram
RUN pip install emoji
RUN pip install CurrencyConverter
RUN pip install requests
RUN pip install environs
RUN pip install redis
RUN pip install apscheduler
RUN pip install aiosqlite
RUN pip install apscheduler-di


# run app
CMD ["python", "main.py"]