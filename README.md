# Классификатор строительных ресурсов BuReClass
Решение [кейса](https://hacks-ai.ru/events/1077375) на хакатоне «Цифровой прорыв. Сезон: искусственный интеллект» в УрФО 17-19 мая 2024 года

## Тизер решения TODO
1. Краткое описание решения (на простом языке, понятном широкому кругу читателей)
2. В одну строчку технические особенности
3. Уникальность вашего решения в одну строку

## Сборка и запуск приложения

**dev-окружение**
```powershell
docker compose --env-file .env --file docker-compose-local.yml up --build
```

**prod-окружение**
```powershell
docker compose --env-file .env up --build
```

Документация конечных точек API представлена в [файле ... TODO]()

## Системные требования TODO (посмотреть в докере)
### Минимальные
* CPU
* RAM
* Disk Space

### Рекомендуемые
* CPU
* RAM
* VRAM
* Disk Space

## Используемые технологии
* Модель: ElasticSearch, SentenceTransformer
* API: FastAPI, Uvicorn, Nginx
* Frontend: Vue.js

From [MOAD.dev](https://moad.dev/) to [Amethyst Capital](https://amethystcapital.ru/) with <3
