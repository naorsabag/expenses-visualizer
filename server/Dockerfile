FROM python:3.7

WORKDIR /usr/src/app

COPY /dependencies/requirements.txt ./

RUN pip install -r requirements.txt

COPY /src ./

CMD [ "python","-u", "app.py" ]
