FROM python:3.7

WORKDIR /usr/src/app

COPY /src ./
COPY /expences.xlsx ./

RUN pip install -r requirements.txt

CMD [ "python","-u", "app.py" ]
