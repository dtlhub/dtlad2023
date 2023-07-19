# Path traversal

### Уязвимость

Все взаимодействия с файловой системой (файл [workspaceUtils.js](/services/amogus_plus_plus/web/src/lib/server/workspaceUtils.js)) никаким образом не санитизируют путь, а параметр `filename` в большинстве запросов контролируем мы. Таким образом, можно подняться по файловой системе на уровень вверх и прочитать файл из воркспейса другого пользователя. Айди воркспейса находится в атак дате.

### Фикс

Добавить фильтрацию имени файлов. Например, можно изменить функцию `getFilePath`, чтобы она выглядела следующим образом:

```js
function getFilePath(workspaceId, filename) {
  if (filename.includes("..") || filename.includes("/")) {
    throw new Error("Bad filename");
  }
  const workspaceDir = getWorkspaceDir(workspaceId);
  return path.join(workspaceDir, filename);
}
```
