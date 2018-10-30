FROM python:3.6.5-alpine3.7

# ディレクトリを移動する
ADD . /app
WORKDIR /app
RUN apk update && apk add git vim
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV PORT 5000
ENV FLASK_APP app.py

# CMD ["python","app.py"]
CMD flask run -h 0.0.0.0 -p $PORT
