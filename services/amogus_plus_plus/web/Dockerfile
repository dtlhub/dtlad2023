FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json /app/
RUN npm ci

COPY . .
RUN npm run build
RUN npm prune --production


FROM node:20-alpine

WORKDIR /app
RUN chown node:node /app
USER node

COPY --from=builder --chown=node:node /app/build build/
COPY --from=builder --chown=node:node /app/node_modules node_modules/
COPY package.json .

ENV NODE_ENV=production

USER root
COPY entrypoint.sh /entrypoint.sh
CMD ["/entrypoint.sh"]
