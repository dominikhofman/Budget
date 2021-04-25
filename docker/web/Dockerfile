FROM python:3.9

# Timezone stuff
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y vim python3-pip

# force stdout and stderror to be unbuffered
ENV PYTHONUNBUFFERED 1

# prepare code folder
RUN mkdir /code
WORKDIR /code

# install python packages
COPY requirements.txt /code/
RUN pip3 install --disable-pip-version-check --no-cache-dir -r requirements.txt

CMD ["tail", "-f", "/dev/null"]

