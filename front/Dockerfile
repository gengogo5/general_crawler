FROM node:12.18.0-alpine3.11

ENV HOME="/app" \
    LANG=C.UTF-8 \
    TZ=Asia/Tokyo 

WORKDIR ${HOME}

RUN apk update && \
    apk upgrade && \
    npm install -g npm && \
    npm install -g @vue/cli \
    npm i @nuxtjs/apollo

ENV HOST 0.0.0.0
EXPOSE 3000
