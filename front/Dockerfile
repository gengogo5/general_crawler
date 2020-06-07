FROM node:14.4.0-alpine3.11

ENV HOME="/app" \
    LANG=C.UTF-8 \
    TZ=Asia/Tokyo 

WORKDIR ${HOME}

RUN apk update && \
    apk upgrade && \
    npm install -g npm && \
    npm install -g @vue/cli

ENV HOST 0.0.0.0
EXPOSE 3000
