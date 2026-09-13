# Копия лендинга re:device — твой вариант

Статический сайт (HTML + CSS + JS + картинки), ничего серверного. Лежит на GitHub Pages бесплатно.

## Быстрый старт

1. Открой `config.json` — там все твои данные (бренд, телефон, город, адрес, карта, заявки).
2. Запусти сборку:
   ```
   python build.py
   ```
3. Посмотри локально:
   ```
   cd docs && python -m http.server 8000
   ```
   Открой http://localhost:8000

## Что подменяется автоматически

| Что | Где в конфиге |
|---|---|
| Название бренда (103 места) | `brand` |
| Телефон во всех форматах | `phonePretty`, `phoneRaw` |
| Email | `email` |
| Город по падежам (Москва/Москве/Москвы...) | `city` |
| Адрес и координаты на карте | `address`, `geo` |
| Время работы | `workHours` |
| Рейтинг и кол-во оценок | `rating`, `reviews` |
| Теглайн у логотипа | `tagline` |
| Ссылки на несуществующие страницы | `internalLinks` (по умолчанию `#`) |
| Логотип (текстовый) | `logo` |
| Open Graph картинка и фавикон | генерируются автоматически под бренд |

Чужие счётчики (Яндекс.Метрика, Google Analytics) вырезаны. Свои — добавь в `counters`.

## Куда летят заявки с форм

Оригинал отправлял их на свой сервер (`/sendform`). На статике такого нет. Выбери в `config.json` → `leads.mode`:

- **`telegram`** (рекомендую): заявка прилетает тебе в телегу.
  1. Напиши @BotFather → `/newbot` → получи токен
  2. Вставь токен в `telegramBotToken`
  3. Напиши @userinfobot → получи свой `Id` → вставь в `telegramChatId`
- **`endpoint`**: любой URL, принимающий POST (Formspree, свой сервер) → `endpoint`
- **`mailto`**: открывает почтовый клиент с готовым письмом (запасной)

## Политика и согласие

Под формы автоматически генерируются `docs/politika.html` и `docs/soglasie.html` — соответствуют ФЗ-152. Редактировать в `policy.py`.

## Деплой на GitHub Pages

Способ 1 — скриптом (нужен [GitHub CLI](https://cli.github.com/)):
```
gh auth login
bash deploy.sh
```
Скрипт сам создаст репозиторий, запушит и включит Pages.

Способ 2 — руками:
1. Создай пустой репозиторий на github.com
2. Settings → Pages → Source: **Deploy from a branch** → branch `main`, folder **`/docs`**
3. В папке сайта:
   ```
   git init
   git add .
   git commit -m "site"
   git remote add origin https://github.com/ТВОЙ-ЛОГИН/РЕПО.git
   git push -u origin main
   ```

Сайт будет на `https://ТВОЙ-ЛОГИН.github.io/РЕПО/`. Впиши этот адрес в `config.json` → `siteUrl` и пересобери.

## Свой домен

Впиши домен в `config.json` → `domain` (создастся `CNAME`), у регистратора добавь A-записи:
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```
и в настройках Pages укажи свой домен.

## Структура

```
build.py          — сборщик
config.json       — твои данные
render_brand.py   — генерация og-картинки и фавикона (нужен Playwright)
policy.py         — генерация политики и согласия (ФЗ-152)
src/              — исходник и ассеты (не трогай)
docs/             — готовый сайт → деплоится на GitHub Pages
check.py          — проверка битых ссылок
deploy.sh         — пуш на GitHub
```