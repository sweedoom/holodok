# -*- coding: utf-8 -*-
"""Генератор политики конфиденциальности и согласия на обработку ПД."""
import os, json, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
cfg = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))

B = cfg["brand"]
PHONE = cfg["phonePretty"]
EMAIL = cfg["email"]
CITY_N = cfg["city"]["nom"]
ADDRESS = cfg["address"]


def shell(title, body):
    return (
        "<!doctype html>\n<html lang=\"ru\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        f"<title>{title} — {B}</title>\n"
        "<meta name=\"robots\" content=\"noindex,nofollow\">\n"
        "<link rel=\"icon\" href=\"public/images/icons/favicon.png\">\n"
        "<style>body{font-family:Arial,Helvetica,sans-serif;max-width:780px;margin:40px auto;padding:0 20px;line-height:1.6;color:#222}"
        "h1{font-size:26px;margin-bottom:8px}h2{font-size:18px;margin-top:28px}"
        ".muted{color:#777}a{color:#00966D}"
        ".back{display:inline-block;margin-bottom:20px;text-decoration:none;color:#00966D}</style>\n"
        "</head>\n<body>\n"
        "<a class=\"back\" href=\"index.html\">\u2190 на главную</a>\n"
        f"<h1>{title}</h1>\n"
        f"<p class=\"muted\">Дата публикации: {cfg.get('policyDate','2026-09-13')}</p>\n"
        f"{body}\n<hr>\n"
        f"<p class=\"muted\">{B} \u00b7 {PHONE} \u00b7 <a href=\"mailto:{EMAIL}\">{EMAIL}</a> \u00b7 {ADDRESS}</p>\n"
        "</body></html>\n"
    )


POLITIKA = (
    "<p>Настоящая Политика обработки персональных данных составлена в соответствии с ФЗ-152 «О персональных данных» и определяет порядок обработки ПД, а также меры по обеспечению их безопасности, предпринимаемые " + B + " (далее — «Оператор»).</p>"
    "<h2>1. Какие данные мы обрабатываем</h2><ul>"
    "<li>Имя (при добровольном указании)</li>"
    "<li>Номер телефона</li>"
    "<li>Текст сообщения</li>"
    "<li>IP-адрес, cookies, данные о браузере и устройстве</li></ul>"
    "<h2>2. Цели обработки</h2><ul>"
    "<li>Приём и обработка заявок на ремонт</li>"
    "<li>Связь с клиентом: подтверждение, согласование времени и стоимости</li>"
    "<li>Улучшение качества обслуживания</li></ul>"
    "<h2>3. Правовые основания</h2><p>Обработка осуществляется на основании согласия субъекта ПД, выражаемого путём отправки формы (ст. 6 ФЗ-152).</p>"
    "<h2>4. Сроки хранения</h2><p>ПД хранятся не дольше, чем этого требуют цели обработки, и уничтожаются по их достижении или при отзыве согласия. Срок хранения заявок — 3 года.</p>"
    "<h2>5. Передача третьим лицам</h2><p>Оператор не передаёт ПД третьим лицам, кроме случаев, предусмотренных законодательством. Для уведомлений может использоваться Telegram.</p>"
    "<h2>6. Защита данных</h2><p>Применяются необходимые правовые, организационные и технические меры для защиты ПД.</p>"
    "<h2>7. Права субъекта ПД</h2><p>Вы вправе получить информацию об обработке, потребовать уточнения/блокирования/уничтожения данных, отозвать согласие — письмом на " + EMAIL + ".</p>"
    "<h2>8. Cookies</h2><p>Сайт использует cookies для корректной работы (в т.ч. Яндекс.Карт). Отключение в браузере может влиять на функции.</p>"
    "<h2>9. Контакты</h2><p>" + EMAIL + ", " + PHONE + ", " + CITY_N + ", " + ADDRESS + ".</p>"
)

SOGLASIE = (
    "<p>Отправляя форму на сайте, вы подтверждаете, что ознакомились с <a href=\"politika.html\">Политикой обработки ПД</a> и даёте согласие на обработку ПД в порядке и на условиях, в ней изложенных.</p>"
    "<h2>Перечень данных</h2><ul><li>имя, номер телефона, текст обращения</li></ul>"
    "<h2>Цели обработки</h2><ul><li>приём заявок, связь с клиентом, согласование времени и стоимости</li></ul>"
    "<h2>Способы обработки</h2><p>Сбор, запись, систематизация, накопление, хранение, уточнение, использование, передача, блокирование, удаление, уничтожение.</p>"
    "<h2>Срок действия согласия</h2><p>С момента отправки формы и до отзыва. Отзыв — письмом на " + EMAIL + ".</p>"
)

def main():
    open(os.path.join(OUT, "politika.html"), "w", encoding="utf-8").write(
        shell("Политика обработки персональных данных", POLITIKA))
    open(os.path.join(OUT, "soglasie.html"), "w", encoding="utf-8").write(
        shell("Согласие на обработку персональных данных", SOGLASIE))
    print("[policy] politika.html + soglasie.html готовы")

if __name__ == "__main__":
    main()