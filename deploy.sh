#!/bin/sh
# cp Dockerfile Dockerfile_bk
# sed -e 's/# CMD/CMD/g' Dockerfile > Dockerfile_tmp
# mv Dockerfile_tmp Dockerfile
pip freeze > requirements.txt
heroku container:push --app mdst-bot web
heroku container:release --app mdst-bot web
heroku config:push --app mdst-bot
# sed -e 's/CMD/# CMD/g' Dockerfile > Dockerfile_tmp
# mv Dockerfile_tmp Dockerfile
docker rmi `docker images -f "dangling=true" -q`
