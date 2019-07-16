FROM python:3

WORKDIR /usr/src/app

COPY /src ./
COPY /expences.xlsx ./

RUN pip install -r requirements.txt

HEALTHCHECK --timeout=2m CMD curl -fsSL "http://loclhost:9200/_cat/health?h=status" | grep -E '^green'

CMD [ "python", "app.py" ]
