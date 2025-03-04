# БИМС МПИТ BACKEND

## Запуск контейнера

`docker-compose build`

`docker-compose up`

## Технические моменты

- **Выбор технологий:**

  - **Backend:** Используется [FastAPI](https://fastapi.tiangolo.com/);
  - **ORM:** Применяется [SQLAlchemy](https://www.sqlalchemy.org/);параметризованных запросов.
  - **База данных:** PostgreSQL выбран за надежность, масштабируемость и поддержу современных механизмов безопасности.

- Реализованы эндпоинты для регистрации, аутентификации, управления профилем, публикации новостей, управления документами и логирование действий.
- Автоматически генерируемая документация OpenAPI (Swagger UI) обеспечивает прозрачность и удобство тестирования API.

- Реализована логика маршрутизации и управления сессиями, обеспечивающая непрерывный и логичный пользовательский путь от входа до выполнения ключевых операций.
- Используются защищённые cookies (HttpOnly, Secure, SameSite) для хранения токенов аутентификации, что обеспечивает стабильное взаимодействие пользователя с системой.

- Прототип готов к развёртыванию с использованием Docker-контейнеров, что обеспечивает переносимость и удобство масштабирования.
- Создан ci cd

- Используем Redis для кеширования

- Применяются проверенные криптографические библиотеки для защиты чувствительных полей.

  - Ограничение числа запросов для предотвращения атак типа brute-force и DDoS.

- **Аудит:**

  - Реализовано структурированное логирование ключевых операций и действий пользователей.
  - Логи записываются в файл для последующего анализа и аудита.

- **Разграничение прав:**
  - Применение политики наименьших привилегий для пользователей и приложений при доступе к базе данных.
- **Защита запросов:**
  - Использование подготовленных запросов (prepared statements) и ORM для предотвращения SQL-инъекций.

TODO
FRONT: валидация синетизация
`
HTML-сущности:

```
< заменяется на &lt;
> заменяется на &gt;
& заменяется на &amp;
" заменяется на &quot;
' заменяется на &#x27; или &apos;
```

BACKEND:
