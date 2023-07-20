FROM ubuntu:20.04

RUN mkdir -p /service/users

WORKDIR /service/

COPY ./server ./server

ENTRYPOINT [ "./server" ]
