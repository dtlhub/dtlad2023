# PocketBase API rules missconfiguration

### Уязвимость

В конфигурации правил доступа PocketBase была допущена ошибка. Для коллекции `workspaces` установленные правила выглядят следующим образом:

```
List/Search: @request.auth.id != ''
View: @request.auth.id != ''
Create: @request.auth.id != ''
Delete: @request.auth.id != ''
```

Как видно, исполнять операции с коллекцией может любой авторизованный юзер. А это значит, что зарегестрировавшись, можно получить полный доступ к коллекции `workspaces`, в том числе к чтению поля `description`, которое содержит флаги.

### Фикс

Изменить правила на `@request.auth.id = owner`.
