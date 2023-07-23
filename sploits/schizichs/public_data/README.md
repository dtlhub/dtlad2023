# Уязвимость

## Программист идиот

При запросе на главную страницу `http://IP:PORT/` в ответ передавался массив данных о лабораторных работах, находящейся в переменной `publicResults` ответа от сервера. Однако массив содержал не только публичные данные, но данные всей лабораторной целиком.
```go
func (lc *LabResultsController) GetLabs() []LabResult {
	var publicResults []LabResult
	lc.db.Find(&publicResults)
	return publicResults
}
...
func showMainPage(g *gin.Context) {
	publicResults := labController.GetLabs()
	render(g, "index.html", gin.H{"header": "Home page", "publicResults": publicResults})
}
```
Таким образом изначально можно было получать данные всех лабораторных работ.

[Код эксплойта](./info_exp.py)

# Фикс

Структура `labResults` уже включает в себя анонимно `publicResults`, поэтому достаточно было поменять функцию `GetLabs()`, чтобы она возвращала массив только публичных даннных лабораторных работ.