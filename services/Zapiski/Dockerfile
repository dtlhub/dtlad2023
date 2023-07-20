FROM ubuntu:latest

RUN mkdir -p /service/users

WORKDIR /service/

COPY ./server ./server

ENTRYPOINT [ "./server" ]
