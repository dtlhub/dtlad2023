#include "game.h"
#include <sys/socket.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

char *Welcome        = "Welcome to ultimate note vault ver 0.3\nSelect your choice:\n1.Login\n2.Register\n>";
char *Login          = "****LOGIN****\nEnter your password: ";
char *Register1      = "**REGISTER***\nRemember that maximum login length is 7\nEnter login: ";
char *Register2      = "Now you can login!!!\nYour password: ";
char *Register3      = "User already exists :(\nTry to login\n";
char *Write          = "Write your note here: ";
char *Read           = "Enter your note id: ";
char *Loading        = "Loading...\n";
char *Loading_failed = "Failed\n";
char *OutUsers       = "YES!!!You did it! Here is your PWN CROWN\nNow enter something you want to be executed in shell: ";

struct Notes{
    char **notes;
    int count;
    char username[9];
};

void prepare(char *login, char* password){
    unsigned key = *((unsigned*)(&login[4]));
    srand(*(unsigned*)(login));
    unsigned box = rand(), i = 0;
    for(;i < 13;i++)
        box ^= rand();
    box ^= key;
    sprintf(password,"%x", box);
}

void save(FILE* fd, struct Notes* notes){
    fwrite(notes->username, 8, 1, fd);
    fwrite((char*)&notes->count, 4, 1, fd);
    int i;
    for(i = 0; i < notes->count; i++) {
        fwrite(notes->notes[i], strlen(notes->notes[i]), 1, fd);
        fwrite("\0", 1, 1, fd);
    }
}

int create_user(char *login, char *filename){
    char fullpath[128];
    sprintf(fullpath, "users/%s", filename);
    if(!access(fullpath, F_OK))
        return 0;
    FILE* fd;
    fd = fopen(fullpath, "w");
    if(fd == NULL)
        return -1;
    struct Notes *notes = calloc(1, sizeof(struct Notes));
    memcpy(notes->username, login, 8);
    save(fd, notes);
    fclose(fd);
    free(notes);
    return 1;
}

struct Notes* load(char *path){
    FILE* fd = fopen(path, "r");
    if(fd == NULL)
        return NULL;
    struct Notes *ret = calloc(1, sizeof(struct Notes));
    fread(ret->username, 8, 1, fd);
    ret->username[8] = '\0';
    fread(&ret->count, 4, 1, fd);
    int i; char a = 1;
    ret->notes = calloc(ret->count, sizeof(char*));
    for(i = 0;i < ret->count;i++)
    {
        char *new_str = NULL; int len = 0;
        do {
            len++;
            fread(&a, 1, 1, fd);
            new_str = realloc(new_str, len);
            new_str[len - 1] = a;
        }while(a != 0);
        a = 1;
        ret->notes[i] = new_str;
    }
    fclose(fd);
    return ret;
}

void win(int out) {
    char buf[1024];
    send(out, OutUsers, strlen(OutUsers), 0);
    recv(out, buf, sizeof buf, 0);
    buf[strlen(buf) - 1] = 0;
    execle("/bin/sh", buf);
}   

void writeNote(int out, struct Notes *user){
    char number[26] = {0};
    if(user->count > 5){
        send(out, "NOPE\n", 5, 0);
        return;
    }
    user->count++;
    user->notes = realloc(user->notes, sizeof(char*)*user->count);
    user->notes[user->count - 1] = calloc(1024, 1);
    send(out, Write, strlen(Write), 0);
    recv(out, user->notes[user->count - 1], 1337, 0);
    user->notes[user->count - 1][strlen(user->notes[user->count - 1]) - 1] = 0;
    user->notes[user->count - 1] = realloc(user->notes[user->count-1], strlen(user->notes[user->count-1]));
    sprintf(number, "%d\n", user->count - 1);
    send(out, number, strlen(number), 0);
}
void readNote(int out, struct Notes *user) {
    if(user->count == 0){
        send(out, "NOPE\n", 5, 0);
        return;
    }
    char buf[10], bbuf[256]; int id;
    send(out, Read, strlen(Read), 0);
    recv(out, buf, sizeof buf, 0);
    buf[strlen(buf) - 1] = 0;
    sscanf(buf, "%d", &id);
    if(id > user->count)
        send(out, "NOPE", 4, 0);
    else
        send(out, user->notes[id], strlen(user->notes[id]), 0);
    send(out, "\n", 1,0);
    
}
void clean(struct Notes *arr){
    int i = 0;
    for(;i < arr->count;i++)
        free(arr->notes[i]);
    free(arr->notes);
    free(arr);
}
void main_loop(int out, struct Notes *user)
{
    char buf[256] = {0};
    char in[1] = {0};
    char fullpath[128] = {0};
    char hello[10] = {0};
    sprintf(buf, "Hello, %s!\n1.Write Note\n2.Read Note\n>", user->username);
    do{
        send(out, buf, 256, 0);
        recv(out, in, 2, 0);
        switch(in[0]){
            case '1':
                writeNote(out, user);
                break;
            case '2':
                readNote(out, user);
                break;
            default:
            prepare(user->username, hello);
            sprintf(fullpath, "users/%s", hello);
            FILE* fd = fopen(fullpath, "w");
            save(fd, user);
            fclose(fd);
            clean(user);
            return;
        }
    }while(1);
}

void Glogin(int out)
{
    char code[21] = {0}, fullpath[128] = {0};
    send(out, Login, strlen(Login), 0);
    recv(out, code, sizeof code, 0);
    code[strlen(code) - 1] = 0;
    sprintf(fullpath, "users/%s", code);
    if(access(fullpath, F_OK))
    {
        printf("ACHTUNG!!!\n%s12",fullpath);
        return;
    }
    send(out, Loading, strlen(Loading), 0);
    struct Notes *user = load(fullpath);
    if(user == NULL) {
        send(out, Loading_failed, strlen(Loading_failed), 0);
        return;
    }
    main_loop(out, user);
}
int check_exists(char *filename){
    char fullpath[128];
    sprintf(fullpath, "users/%s", filename);
    return access(fullpath, F_OK);
}
void Gregister(int out)
{
    char login[8] = {0}, password[10] = {0};
    send(out, Register1, strlen(Register1), 0);
    recv(out, login, sizeof login, 0);
    login[strlen(login) - 1] = 0;
    prepare(login, password);
    if(create_user(login, password)) {
        send(out, Register2, strlen(Register2), 0);
        send(out, password, sizeof password,0);
        send(out, "\n", 1,0);
    } else {
        send(out, Register3, strlen(Register3), 0);
    }
}

int game(int out){
    char recive_buf[4];
    send(out, Welcome, strlen(Welcome), 0);
    recv(out, recive_buf, sizeof recive_buf, 0);
    switch(recive_buf[0])
    {
        case '2':
            Gregister(out);
        case '1':
            Glogin(out);
            break;
        default:
            return 1;
    }
    return 0;
}