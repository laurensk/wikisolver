# Base

FROM node:16-alpine AS base

# Build

FROM base AS build

WORKDIR /app

COPY . .

RUN npm i
RUN npm run build

# Caddy

FROM caddy:latest as caddy

COPY --from=build /app/dist/wikisolver-client /usr/share/caddy

RUN echo ":80\n\
\n\
root * /usr/share/caddy\n\
file_server" > /etc/caddy/Caddyfile

EXPOSE 80

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
