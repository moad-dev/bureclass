Актуализация базы наименований строительных ресурсов. Принимает excel (.xlsx) файл классификатора строительных ресурсов, доступный по адресу https://fgiscs.minstroyrf.ru/ksr

Route: ```/api/actualize```

Method: POST

Body:

Content type: multipart/form-data

|field|type|description|Required|
|-----|----|-----------|--------|
|file |file|.xlsx file, mimetype: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet|true|
|password|file|Пароль администратора|true|

Response 202:
    
Response 400: \
Content type: application/json
```
{
    "detail": "Invalid document type"
}
```

Response 403: \
Content type: application/json
```
{
    "detail": "Invalid credentials"
}
```

---

Определение нескольких строительных ресурсов, наименование которых похоже на заданное.

Route: ```/api/search```

Method: GET

Parameters:

|Name       |type  |description|Required|
|-----------|------|-----------|--------|
|object_name|string|Потенциально неправильное наименование продукта|true|
|limit      |number|Ограничение на число возвращаемых кандидатов|true|
    
Response 200: \
Content type: application/json
```
[
    {
        "code": string,
        "object_name": string,
        "score": float
    },
    ...
]
```

---

Полуение состояния выполнения задачи актуализации данных.

Route: ```/api/actualize```

Method: GET

Response 200 \
Content type: application/json
```
{
    status: ('running'|'completed'|'failed')
}
```
