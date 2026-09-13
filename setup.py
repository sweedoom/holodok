# -*- coding: utf-8 -*-
"""
Мастер настройки: задаёт вопросы, пишет config.json, сразу собирает сайт.
Запуск:  python setup.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(ROOT, "config.json")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

cfg = json.load(open(CFG, encoding="utf-8"))


def ask(q, default=""):
    d = f" [{default}]" if default else ""
    v = input(f"{q}{d}: ").strip()
    return v if v else default


def pretty(phone):
    d = re.sub(r"\D", "", phone)
    if d.startswith("8"):
        d = "7" + d[1:]
    if len(d) != 11:
        return phone
    return f"+7 ({d[1:4]}) {d[4:7]}-{d[7:9]}-{d[9:11]}"


def cases(city):
    """Черновые падежи — пользователь подтверждает/правит."""
    c = city.strip()
    low = c.lower()
    if low.endswith(("а", "я")) and not low.endswith(("ия", "ея")):
        gen, prep = c[:-1] + ("и" if low.endswith("я") else "ы"), c[:-1] + "е"
    elif low.endswith("ь"):
        gen, prep = c[:-1] + "я", c[:-1] + "е"
    else:
        gen, prep = c + "а", c + "е"
    return {"nom": c, "gen": gen, "prep": prep, "acc": c, "abl": c}


print("=" * 60)
print("НАСТРОЙКА САЙТА — отвечай на вопросы, Enter = вариант по умолчанию")
print("=" * 60)

cfg["brand"] = ask("Название бренда", cfg["brand"])
cfg["tagline"] = ask("Теглайн у логотипа", cfg.get("tagline", "Сервисный центр"))

phone = ask("Телефон (любой формат)", cfg["phonePretty"])
cfg["phonePretty"] = pretty(phone)
cfg["phoneRaw"] = "+7" + re.sub(r"\D", "", phone)[-10:]

cfg["email"] = ask("Email", cfg["email"])

city = ask("Город (именительный: Москва, Казань...)", cfg["city"]["nom"])
if city != cfg["city"]["nom"] or True:
    cc = cases(city)
    print("  Проверь падежи города (в скобках — как обычно пишут 'в ...'):")
    cc["gen"] = ask("   родительный (у Москвы)", cc["gen"])
    cc["prep"] = ask("   предложный (в Москве)", cc["prep"])
    cc["acc"] = ask("   винительный (в Москву)", cc["acc"])
    cc["abl"] = ask("   творительный (Москвой)", cc["abl"])
    cfg["city"] = cc

cfg["address"] = ask("Адрес (ул. Ленина, 15)", cfg["address"])

geo = ask("Координаты карты 'широта,долгота' (Enter — оставить текущие)", "")
if geo and "," in geo:
    lat, lon = geo.split(",")
    cfg["geo"] = {"lat": float(lat.strip()), "lon": float(lon.strip())}
else:
    print(f"  оставляю {cfg['geo']['lat']}, {cfg['geo']['lon']} — потом поправишь в config.json")

cfg["workHours"] = ask("Время работы (текстом)", cfg["workHours"])
cfg["openingHours"] = ask("Время работы для schema.org (Mo-Su 09:00-21:00)", cfg["openingHours"])

print("\nКУДА ПРИСЫЛАТЬ ЗАЯВКИ:")
print("  1) telegram — в бота (нужны токен и chat_id)")
print("  2) endpoint — POST на свой URL (Formspree и т.п.)")
print("  3) mailto   — открывать почтовик")
mode = ask("Режим (1/2/3)", "1")
cfg["leads"]["mode"] = {"1": "telegram", "2": "endpoint", "3": "mailto"}.get(mode, "telegram")
if cfg["leads"]["mode"] == "telegram":
    cfg["leads"]["telegramBotToken"] = ask("  Токен бота (@BotFather)", cfg["leads"]["telegramBotToken"])
    cfg["leads"]["telegramChatId"] = ask("  Chat ID (@userinfobot)", cfg["leads"]["telegramChatId"])
elif cfg["leads"]["mode"] == "endpoint":
    cfg["leads"]["endpoint"] = ask("  URL для POST", cfg["leads"]["endpoint"])

site = ask("Адрес сайта (https://логин.github.io/репо/)", cfg["siteUrl"])
cfg["siteUrl"] = site if site.endswith("/") else site + "/"

dom = ask("Свой домен (Enter — пока без домена)", cfg.get("domain", ""))
if dom:
    cfg["domain"] = dom
elif "domain" in cfg:
    del cfg["domain"]

json.dump(cfg, open(CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n[config] config.json обновлён")

print("\n[build] собираю сайт...")
r = subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], cwd=ROOT)
if r.returncode == 0:
    print("\n✓ ГОТОВО. Сайт в папке docs/")
    print("  Задеплой:  gh auth login  →  bash deploy.sh")
else:
    print("\n✗ Сборка упала — смотри ошибки выше")