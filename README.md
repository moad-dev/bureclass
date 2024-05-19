# Классификатор строительных ресурсов BuReClass
Решение [кейса](https://hacks-ai.ru/events/1077375) на хакатоне «Цифровой прорыв. Сезон: искусственный интеллект» в УрФО 17-19 мая 2024 года.

## Тизер решения
При составлении технической документации и закупках необходимо указывать строительные материалы и ресурсы в соответствии с официальным Классификатором строительных ресурсов (КСР). Решение представляет собой веб-сервис с API для автоматизированного подбора официального наименования и кода строительного ресурса на основании произвольного названия. 

Технической особенностью является индексация КСР с помощью современного свободно распространяемого поискового движка ElasticSearch. Уникальностью решения является использование модели Sentence BERT [`MOADdev/multilingual-e5-large-amethyst`](https://huggingface.co/MOADdev/multilingual-e5-large-amethyst), дообученной на текстах предметной области строительства, что позволяет актуализировать индексацию КСР без модификации поисковых средств.

## Сборка и запуск приложения
```powershell
docker compose --env-file .env up --build
```

Документация конечных точек API представлена в [файле API-DOCUMENTATION.md](API-DOCUMENTATION.md). Материалы исследований моделей искусственного интеллекта находятся в директории [research](research).

## Минимальные системные требовани
* CPU: 2 ядра, 2 ГГц
* RAM: 12 ГБ
* Disk Space: 30 ГБ

## Используемые технологии
* Интеллектуальный подбор наименований: ElasticSearch, SentenceTransformer;
* API: FastAPI, Uvicorn, Nginx;
* Frontend: Vue.js.

From [MOAD.dev](https://moad.dev/) to [Amethyst Capital](https://amethystcapital.ru/) with <3
