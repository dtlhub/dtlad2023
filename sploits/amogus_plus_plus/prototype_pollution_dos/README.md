# Prototype pollution DoS

### Дисклеймер-факап

На самом деле сервис проектировался вокруг этой уязвимости, однако на завершающем этапе разработки оказалось, что она не эксплуатируема. Происходит это из-за того, что при любом заражении прототипа в PocketBase JS-SDK есть несколько мест, в которых объекты создаются небезопасным образом. Это приводит к различным ошибкам. Например, если в окружении заражен прототип, при попытке зафетчить любой объект переполнится стэк вызовов.

> Стэк вызовов переполняется из-за того, что [тут](https://github.com/pocketbase/js-sdk/blob/283499d912b1c4793649ebd730ac6bed069106bc/src/models/Record.ts#L26) при итерации по `expand` используются также и ключи прототипа, что приводит к бесконечному рекурсивному вызову `_loadExpand`.

Однако было принято решение оставить уязвимость, потому что, несмотря на то, что с её помощью не выйдет украсть флаги, она позволяет устроить DoS сервисов оппонентов, понизив таким образом их SLA, что приведет к поднятию в рейтинге.

### Уязвимость

Уязвимость формируется из нескольких независимых ошибок:

- [runtime.js](/services/amogus_plus_plus/web/src/lib/server/amogus_plus_plus/runtime.js), добавление новых объектов в `Runtime._storage` происходит с использованием небезопасной реализации функции `merge`. Она позволяет заразить прототип, если передать в функцию `Runtime.addToStorage(value)` `value` вида `{__prototype__: {...}}`
- [statementBases.js](services/amogus_plus_plus/web/src/lib/amogus_plus_plus/statementsBases.js): конвертирование из строки в число происходит не с помощью функции `parseInt`, а с использованием `JSON.parse`, что позволяет парсить не только число, а, в принципе, любой json-serializable объект.
- [statementBases.js](services/amogus_plus_plus/web/src/lib/amogus_plus_plus/statementsBases.js): регулярное выражение для числа такое же, как и для имен переменных/файлов. Поэтому есть возможность присвоить переменной значение не только числа, но и чего-нибудь другого.

Таким образом, возможно заразить прототип, исполнив скрипт вида:

```
GUYS I CAN VOUCH __proto__ IS {"foo":"bar"}
```

Что приведет к ошибке в PocketBase JS-SDK.

### Фикс

Можно пофиксить любой из этапов эксплуатации. Самый простой, пожалуй - заменить использование `JSON.parse` на `parseInt`, что не позволит присвоить переменной значение произвольного объекта, не являющегося числом.