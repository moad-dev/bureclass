# Классификатор строительных ресурсов BuReClass

Решение [кейса](https://hacks-ai.ru/events/1077375) на хакатоне «Цифровой прорыв. Сезон: искусственный интеллект» в УрФО 17-19 мая 2024 года

## Решение


## СБорка и запуск dev-окружения

```powershell
docker compose --env-file .env --file docker-compose-local.yml build
docker compose --env-file .env --file docker-compose-local.yml up
```

## Используемые технологии
* Модель: ElasticSearch, SentenceTransformer
* API: FastAPI, Uvicorn, Nginx
* Front-end: Vue.js

From [MOAD.dev](https://moad.dev/) to [Amethyst Capital](https://amethystcapital.ru/) with <3
