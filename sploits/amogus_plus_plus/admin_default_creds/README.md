# Admin default credentials

### Уязвимость

Админка PocketBase имеет дефолтные креды

```
email: admin@admin.com
password: administrator
```

Их можно найти, например, в секции healthcheck контейнера `pocketbase` в файле [docker-compose.yml](/services/amogus_plus_plus/docker-compose.yml):

```yaml
---
healthcheck:
  test: wget --post-data 'identity=admin@admin.com&password=administrator' --no-verbose --tries=1 --spider http://localhost:8090/api/admins/auth-with-password || exit 1
  interval: 5s
  timeout: 5s
  retries: 5
```

Имея доступ к админке можно сдампить таблички users и workspaces, получая флаги из email-ов пользователей и description-ов воркспейсов.

### Фикс

Можно просто зайти в веб-интерфейс админки, который находится на `http://hostname:1984/_/` и ручками изменить пароль.
