CC=clang
CFLAGS=-s -O1 -no-pie -Wl,-z,norelro -fno-stack-protector

all: ./build/game.o ./build/main.o
	$(CC) $(CFLAGS) ./build/game.o ./build/main.o -o servers 

./build/main.o: ./src/main.c
	$(CC) -c ./src/main.c -o ./build/main.o

./build/game.o: ./src/game.c
	$(CC) -c ./src/game.c -o ./build/game.o 