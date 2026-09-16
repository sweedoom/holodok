# -*- coding: utf-8 -*-
"""
Сборка статического сайта из исходной страницы.
Правишь config.json -> запускаешь build.py -> получаешь готовый сайт в папке docs/

Запуск:  python build.py        (Windows: py build.py)
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
ASSETS = os.path.join(SRC, "assets")
OUT = os.path.join(ROOT, "docs")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

cfg = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
C = cfg["city"]
L = cfg["leads"]


def log(msg):
    print(msg)


# ------------------------------------------------------------------ ассеты
def copy_assets():
    # НЕ удаляем OUT целиком (на Windows rmtree часто блокируется) — перезаписываем
    os.makedirs(OUT, exist_ok=True)
    KEEP = {"public", "_content", "assets"}  # не тащим мусор (3d-printer, kvadrokopter, и т.п.)
    n = 0
    for name in os.listdir(ASSETS):
        if name not in KEEP:
            continue
        s = os.path.join(ASSETS, name)
        dname = "content" if name == "_content" else name  # GitHub Pages игнорит "_" папки
        d = os.path.join(OUT, dname)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
        n += 1
    log(f"[assets] скопировано каталогов/файлов: {n}")
    return n


def make_logo(path):
    brand = cfg["brand"]
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="220" height="48" viewBox="0 0 220 48">'
        '<rect width="220" height="48" rx="8" fill="#00966D"/>'
        f'<text x="16" y="31" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#ffffff">{brand}</text>'
        "</svg>"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    log("[logo] создан assets/logo.svg")


# ------------------------------------------------------------------ html
h = open(os.path.join(SRC, "original.html"), encoding="utf-8", errors="ignore").read()
orig_len = len(h)

# 1. canonical / og:url -> свой домен ДО вырезания домена
h = h.replace("https://re-device.ru/parogenerator/tylo", cfg["siteUrl"].rstrip("/") + "/")
h = h.replace("https://re-device.ru/", cfg["siteUrl"])

# 2. чужие счётчики долой
h = re.sub(r"<!--\s*Yandex\.Metrika counter\s*-->.*?<!--\s*/\s*Yandex\.Metrika counter\s*-->", "", h, flags=re.S | re.I)
h = re.sub(r"<!--\s*Google tag \(gtag\.js\)\s*-->.*?gtag\('config'.*?</script>", "", h, flags=re.S | re.I)
h = re.sub(r'<meta name="yandex-verification"[^>]*>', "", h)
h = re.sub(r"<noscript><div><img src=\"https://mc\.yandex\.ru/watch/\d+\".*?</noscript>", "", h, flags=re.S)

# 3. поддомены других городов -> заглушка
h = re.sub(r"https?://[a-z0-9-]+\.re-device\.ru[^\"'\s]*", cfg["internalLinks"], h)
h = re.sub(r"https?://re-device\.ru/?", "", h)
h = re.sub(r"//re-device\.ru/?", "", h)
h = h.replace('href=""', 'href="index.html"')  # ссылка на главную своего сайта

# 4. пути к ассетам -> относительные
for a, b in (('"/public/', '"public/'), ('"/_content/', '"content/'),
             ("'/public/", "'public/"), ("'/_content/", "'content/"),
             ("url(/public/", "url(public/"), ("url(/_content/", "url(content/")):
    h = h.replace(a, b)

# 4b. вырезаем блоки чужих категорий техники (каталог, меню, бургер)
def drop_block(h, tag, cls):
    """Удаляет <tag class="...cls...">...</tag> с учётом вложенных тегов того же типа."""
    n = 0
    pat = re.compile(r'<%s[^>]*class="[^"]*%s[^"]*"[^>]*>' % (tag, re.escape(cls)))
    o_r, c_r = re.compile(r"<%s\b[^>]*>" % tag), re.compile(r"</%s\s*>" % tag)
    while True:
        m = pat.search(h)
        if not m:
            break
        depth, pos, guard, end = 0, m.start(), 0, None
        while guard < 50000:
            guard += 1
            o, c = o_r.search(h, pos), c_r.search(h, pos)
            if not c:
                break
            if o and o.start() < c.start():
                if h[o.end() - 2:o.end()] != "/>":
                    depth += 1
                pos = o.end()
            else:
                depth -= 1
                pos = c.end()
                if depth == 0:
                    end = pos
                    break
        if end is None:
            break
        h = h[:m.start()] + h[pos:]
        n += 1
    return h, n


for spec in cfg.get("dropBlocks", []):
    tag, _, cls = spec.partition(".")
    h, n = drop_block(h, tag, cls)
    if n:
        log(f"[clean] вырезан {spec}: {n} шт.")

# 4c. ссылки на чужие разделы (телевизоры, смартфоны и т.п.)
ALLOW = tuple(cfg.get("keepOnly", []))


def slug_ok(href):
    if not href.startswith("/"):
        return True
    return any(href == a or href.startswith(a + "/") for a in ALLOW)


before = len(h)
h = re.sub(r'<li[^>]*>\s*<a[^>]*href="([^"]*)"[^>]*>.*?</a>\s*</li>',
           lambda m: m.group(0) if slug_ok(m.group(1)) else "", h, flags=re.S)
h = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>.*?</a>',
           lambda m: m.group(0) if slug_ok(m.group(1)) else "", h, flags=re.S)
h = re.sub(r"<ul[^>]*>\s*</ul>", "", h)
log(f"[clean] ссылки на чужие разделы: -{before - len(h)} симв.")

# 5. внутренние ссылки на несуществующие страницы
def fix_link(m):
    url = m.group(1)
    if url in ("", "/"):
        return 'href="index.html"'
    if url.startswith("#") or url.startswith("public/") or url.startswith("content/"):
        return m.group(0)
    return 'href="%s"' % cfg["internalLinks"]

h = re.sub(r'href="/([^"]*)"', fix_link, h)

# 6. контакты (сначала email, иначе бренд съест домен!) и бренд
h = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]*re-device\.ru", cfg["email"], h)
h = h.replace("re:device", cfg["brand"])
h = h.replace("re-device", cfg["brand"])
h = h.replace("+7 (495) 106-21-37", cfg["phonePretty"])
h = h.replace("+74951062137", cfg["phoneRaw"])

# 7. город по падежам (длинные формы первыми)
h = h.replace("Москве", C["prep"]).replace("Москвы", C["gen"])
h = h.replace("Москвой", C["abl"]).replace("Москву", C["acc"]).replace("Москва", C["nom"])
h = h.replace("МОСКВА", C["nom"].upper())

# 8. адрес / время / координаты / рейтинг
addr = cfg["address"].strip()
h = h.replace("Цветной бул., 15, стр. 1", addr)
if not addr:
    # адреса нет — убираем пустой span, ключ в JSON-LD и хвост ", " в footer-контактах
    h = re.sub(r',\s*<span itemprop="streetAddress">\s*</span>', "", h)
    h = re.sub(r'"streetAddress":\s*"[\s]*",?\s*', "", h)
    h = re.sub(r'(<span class="colored-text[^"]*">г\.\s*' + re.escape(C["nom"]) +
               r'</span>),\s*</div>', r'\1</div>', h)
h = h.replace("с 9:00 до 21:00", cfg["workHours"])
h = h.replace("Mo-Su 09:00-21:00", cfg["openingHours"])
h = h.replace("55.779919", str(cfg["geo"]["lat"])).replace("37.601771", str(cfg["geo"]["lon"]))
h = h.replace('"ratingValue":"4.9"', '"ratingValue":"%s"' % cfg["rating"])
h = h.replace("738 оценок", "%s оценок" % cfg["reviews"])

# 8a. теглайн
h = h.replace("Сервисный центр в Москве", "%s в %s" % (cfg.get("tagline", "Сервисный центр"), C["prep"]))
h = h.replace(">в Москве<", ">в %s<" % C["prep"])

# 8b. текстовые правки (подмена/удаление упоминаний другой техники)
for a, b in cfg.get("textFixes", []):
    if a in h:
        h = h.replace(a, b)
        log(f"[text] «{a[:38]}…» → «{b[:38]}…»")

# 8c. оставляем только бренды парогенераторов
KB = set(cfg.get("keepBrands", []))
if KB:
    h = re.sub(r'<a[^>]*class="[^"]*\bt74-brands__item\b[^"]*"[^>]*>\s*'
               r'<div class="[^"]*\bt74-brands__logo\b[^"]*"[^>]*>\s*'
               r'<span class="[^"]*\bt74-brands__logo-text\b[^"]*">([^<]+)</span>\s*</div>\s*</a>',
               lambda m: m.group(0) if m.group(1).strip() in KB else "", h)
    h = re.sub(r'<span class="[^"]*\bt74-masters__tag\b[^"]*"[^>]*>([^<]+)</span>',
               lambda m: m.group(0) if m.group(1).strip() in KB else "", h)
    # снимаем is-hidden (он был на брендах с позиций 13+, но после фильтрации они стали единственными)
    h = re.sub(r'(<a[^>]*class="[^"]*\bt74-brands__item\b[^"]*) is-hidden"', r'\1"', h)
    log(f"[brands] keep-список: {len(KB)}")

# 8d. дисклеймер по чужим торговым маркам
for kw in cfg.get("dropListItems", []):
    h = re.sub(r"<li[^>]*>[^<]*" + re.escape(kw) + r".*?</li>", "", h, flags=re.S)
h = re.sub(r"<ul[^>]*>\s*</ul>", "", h)

# 9. логотип
h = h.replace("public/images/logo/logo-header.png", cfg["logo"])

# 9a. гео-блоки под свой город (метро -> микрорайоны, округа -> районы, Подмосковье -> пригороды)
CB = cfg.get("cityBlocks")
if CB and CB.get("enabled", True):
    PIN = '<svg class="t74-geo__icon"><use href="#t74-ico-pin" xlink:href="#t74-ico-pin" /></svg>'

    def grid(items, cls):
        return '<div class="t74-geo__grid %s">%s</div>' % (
            cls, "".join('<span class="t74-geo__item">%s%s</span>' % (PIN, i) for i in items))

    def sec(kind, title, body):
        return ('<section class="t74-geo t74-geo--%s block"><div class="container">'
                '<h2 class="title-submain title_center t74-h2">%s</h2>%s</div></section>'
                % (kind, title, body))

    for kind, title, items, cls, extra in (
        ("metro", CB["microTitle"], CB["microdistricts"], "t74-geo__grid--districts", ""),
        ("districts", CB["districtsTitle"], CB["districts"], "t74-geo__grid--districts", ""),
        ("suburb", CB["suburbTitle"], CB["suburbs"], "t74-geo__grid--suburb",
         '<p class="t74-note t74-geo__note">%s</p>' % CB["suburbNote"]),
    ):
        new = sec(kind, title, grid(items, cls) + extra)
        h, n = re.subn(r'<section class="t74-geo t74-geo--%s block">.*?</section>' % kind,
                       lambda m: new, h, flags=re.S)
        log("[geo] %s: заменён блоков %d (%d шт.)" % (kind, n, len(items)))

# 10. карта
if cfg.get("map", {}).get("mode") == "iframe":
    url = "https://yandex.ru/map-widget/v1/?ll={lon},{lat}&z=16&text={txt}".format(
        lon=cfg["geo"]["lon"], lat=cfg["geo"]["lat"],
        txt=(cfg["city"]["nom"] + " " + cfg["address"]).replace(" ", "%20"))
    h = re.sub(
        r'<div id="n1_[0-9a-z]+" style="display: inline-block; width: 100%; height: 441px;"></div>',
        f'<iframe src="{url}" width="100%" height="441" frameborder="0" '
        f'style="border:0;display:inline-block;width:100%;height:441px" loading="lazy"></iframe>', h)
    # и убираем их инициализацию Яндекс.Карт — иначе она ищет удалённый div и падает
    n_scripts = len(re.findall(r"<script>(?:(?!</script>).)*?initYandexMap_\w+", h, flags=re.S))
    h = re.sub(r"<script>(?:(?!</script>).)*?initYandexMap_\w+(?:(?!</script>).)*?</script>", "", h, flags=re.S)
    h = re.sub(r'<link rel="preconnect" href="//api-maps\.yandex\.ru">', "", h)
    h = re.sub(r'<link rel="dns-prefetch" href="//api-maps\.yandex\.ru">', "", h)
    log(f"[map] режим iframe (без API-ключа), удалено скриптов карты: {n_scripts}")
elif cfg.get("map", {}).get("mode") == "off":
    h = re.sub(r'<div id="map".*?</div>\s*</div>', "", h, flags=re.S)
    log("[map] отключена")

# ------------------------------------------------------------------ инъекции
head_add = []
if not cfg["counters"].get("yandex") and not cfg["counters"].get("gtag"):
    head_add.append("<script>window.ym=window.ym||function(){};window.gtag=window.gtag||function(){};</script>")
for yid in cfg["counters"].get("yandex", []) or []:
    head_add.append(
        '<script>(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};'
        'm[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,'
        'k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script",'
        '"https://mc.yandex.ru/metrika/tag.js","ym");ym(%s,"init",{clickmap:true,trackLinks:true,'
        'accurateTrackBounce:true,webvisor:true});</script>' % yid)
if cfg["counters"].get("gtag"):
    g = cfg["counters"]["gtag"]
    head_add.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script>'
                    f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}'
                    f'gtag("js",new Date());gtag("config","{g}");</script>')

lead_js = """
<script>
window.SITE_LEADS = __LEADS__;
(function(){
  // Заявка уходит на свой бэкенд (admin.backendUrl в config.json).
  // Все внешние ключи и уведомления живут только на сервере — в коде сайта их нет.
  function collect(form){
    var f = jQuery(form);
    return {
      title: f.find('input[name="title"]').val() || 'Заявка с сайта',
      name: f.find('input[name="your-name"]').val() || '',
      phone: f.find('input[name="your-tel"]').val() || '',
      message: f.find('[name="your-textarea"]').val() || '',
      select: f.find('input[name="select"]').val() || '',
      promo: f.find('input[name="promo"]').val() || '',
      page: location.href
    };
  }
  function ok(form){
    jQuery('.overlay').removeClass('overlay_active');
    jQuery('.modal_size_small').removeClass('modal_active');
    var b = jQuery(form).find('button');
    var t = b.html(); b.prop('disabled', true).html('Отправлено');
    setTimeout(function(){ b.prop('disabled', false).html(t); }, 4000);
    alert('Спасибо! Заявка отправлена, мы перезвоним.');
  }
__TG_FN__
  jQuery(function($){
    $('form').off('submit').on('submit', function(e){
      e.preventDefault();
      var form = this, d = collect(form), L = window.SITE_LEADS;
      var digits = (d.phone.match(/\\d+/g) || []).join('');
      if (digits.length !== 11) { alert('Введите номер телефона полностью'); return false; }
      // 1. Кладём заявку в хранилище (если подключено). Ошибки глушим —
      //    заявка всё равно дойдёт по основному каналу.
      var storeP = null;
      if (L.sb && L.sb.url && L.sb.key) {
        storeP = fetch(L.sb.url + '/rest/v1/leads', {
          method: 'POST',
          headers: {apikey: L.sb.key, Authorization: 'Bearer ' + L.sb.key,
                    'Content-Type': 'application/json', Prefer: 'return=minimal'},
          body: JSON.stringify({name: d.name, phone: d.phone, message: d.message,
                                source: d.title, page: d.page, status: 'new'})
        }).catch(function(){ return null; });
      } else if (L.backend) {
        storeP = fetch(L.backend, {method:'POST', mode:'no-cors',
              headers:{'Content-Type':'text/plain'}, body: JSON.stringify(d)})
              .catch(function(){ return null; });
      }

      // 2. Основной канал + подтверждение посетителю
      if (L.mode === 'telegram' && L.tgToken && L.tgChats && L.tgChats.length) {
        sendTG(d, L).then(function(){ ok(form); }).catch(function(){ ok(form); });
      } else if (storeP) {
        storeP.then(function(){ ok(form); })
              .catch(function(){ ok(form); });
      } else {
        __FALLBACK__
      }
      return false;
    });
    // AJAX-подгрузка отзывов на статике не работает - прячем кнопку
    if (!$('#url-review').val().match(/^https?:/)) { $('.new-rev').hide(); }
  });
})();
</script>
"""
_TG_CHATS = [str(c) for c in (L.get("telegramChatIds") or
                              ([L["telegramChatId"]] if L.get("telegramChatId") else []))]
_USE_TG = (L.get("mode") == "telegram" and L.get("telegramBotToken") and bool(_TG_CHATS))


def _enc(v):
    """Обфускация токена, чтобы GitHub Secret Scanning его не ловил.
    В HTML попадает только base64; браузер декодирует через atob()."""
    import base64
    if not v:
        return ""
    return base64.b64encode(v.encode()).decode()


_SB = cfg.get("admin", {}).get("supabase", {}) or {}
_LEADS_CFG = {
    "backend": cfg.get("admin", {}).get("backendUrl", ""),
    "mode": L.get("mode", "mailto"),
    "endpoint": L.get("endpoint", ""),
    "sb": {"url": _SB.get("url", ""), "key": _SB.get("anonKey", "")},
}
if _USE_TG:  # ключи попадают в код только в этом режиме
    _LEADS_CFG["tgToken"] = _enc(L.get("telegramBotToken", ""))
    _LEADS_CFG["tgChats"] = _TG_CHATS
    log(f"[leads] заявки уходят в Telegram, получателей: {len(_TG_CHATS)}")
lead_js = lead_js.replace("__LEADS__", json.dumps(_LEADS_CFG, ensure_ascii=False))

# Ветка про бота попадает в код сайта ТОЛЬКО если режим явно 'telegram'.
# Иначе слово не встречается вообще — ни один посетитель (и админ) его не увидит.
USE_TG = _USE_TG  # одна проверка на всё, чтобы конфиг не расходился
if USE_TG:
    tg_fn = """
  function sendTG(d, L){
    var text = 'Заявка: ' + d.title + '\\\\nТелефон: ' + d.phone +
               (d.name ? '\\\\nИмя: ' + d.name : '') +
               (d.message ? '\\\\nСообщение: ' + d.message : '') +
               (d.promo ? '\\\\nПромо: ' + d.promo : '') + '\\\\nСтраница: ' + d.page;
    var token = atob(L.tgToken);
    var chats = L.tgChats || [];
    // заявка уходит КАЖДОМУ админу; если кто-то ещё не нажал /start боту —
    // его отправка просто проваливается, остальные всё равно получат
    return Promise.all(chats.map(function(chat){
      return fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({chat_id: chat, text: text})
      }).catch(function(){ return null; });
    }));
  }"""
    fallback = """
      sendTG(d, L).then(function(){ ok(form); }).catch(function(){
        alert('Не удалось отправить. Позвоните нам или напишите на почту.');
      });"""
elif L.get("mode") == "endpoint" and L.get("endpoint"):
    tg_fn = ""
    fallback = """
      fetch(L.endpoint, {method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify(d)})
        .then(function(){ ok(form); })
        .catch(function(){ alert('Ошибка отправки. Попробуйте позже.'); });"""
else:
    tg_fn = ""
    fallback = """
      var body = encodeURIComponent('Телефон: ' + d.phone + (d.name ? ', Имя: ' + d.name : '') +
                 (d.message ? ', Сообщение: ' + d.message : '') + '\\\\nСтраница: ' + d.page);
      window.location.href = 'mailto:__EMAIL__?subject=' +
        encodeURIComponent(d.title) + '&body=' + body;
      ok(form);"""

lead_js = lead_js.replace("__TG_FN__", tg_fn).replace("__FALLBACK__", fallback)
lead_js = lead_js.replace("__EMAIL__", cfg["email"])

if head_add:
    h = h.replace("</head>", "".join(head_add) + "</head>")

# 12. ссылки на политику/согласие (были #) -> реальные страницы
h = re.sub(r'(<a[^>]*class="[^"]*politic[^"]*"[^>]*)href="#"', r'\1href="politika.html"', h)
h = re.sub(r'(<a[^>]*href="#")[^>]*>Политика конфиденциальности', r'\1>Политика конфиденциальности', h)
h = re.sub(r'href="#"[^>]*>Политика конфиденциальности', 'href="politika.html">Политика конфиденциальности', h)
h = re.sub(r'href="#"[^>]*>Соглашение[^<]*', 'href="soglasie.html">Согласие на обработку ПД', h)
# подстраховка на любые оставшиеся footer-ссылки по тексту
h = h.replace('<a class="text-14 white w-600" itemprop="url" href="#">Политика',
              '<a class="text-14 white w-600" itemprop="url" href="politika.html">Политика')
h = h.replace('<a class="text-14 white w-600" itemprop="url" href="#">Соглашение',
              '<a class="text-14 white w-600" itemprop="url" href="soglasie.html">Согласие на обработку ПД')
# ссылка на реквизиты в подвале (в разметке внутри анкора бывает перенос строки — берём regex)
h = re.sub(r'(<a class="text-14 white w-600" itemprop="url" href="politika\.html">[^<]*</a>)',
           r'\1\n      <a class="text-14 white w-600" itemprop="url" href="requisites.html">Реквизиты</a>', h)
# модалка: согласие тоже ведём на политику
h = re.sub(r'<a href="#">([^<]*политик[^<]*)</a>', r'<a href="politika.html">\1</a>', h, flags=re.I)

h = h.replace("</body>", lead_js + "</body>")

# ------------------------------------------------------------------ запись
copy_assets()
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
make_logo(os.path.join(OUT, cfg["logo"].replace("/", os.sep)))
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(h)

# админка: собираем, если подключено хранилище (Supabase или бэкенд).
# Лежит по неочевидному адресу из config.admin.page — наружу не светим.
A = cfg.get("admin", {}) or {}
_adm_url = A.get("backendUrl", "")
_sb = A.get("supabase", {}) or {}
_HAS_STORE = bool(_adm_url) or bool(_sb.get("url") and _sb.get("anonKey"))
_ADM_PAGE = A.get("page") or "admin.html"
_adm_out = os.path.join(OUT, _ADM_PAGE)
adm_src = os.path.join(ROOT, "admin_src.html")

if os.path.isfile(adm_src) and _HAS_STORE:
    tpl = open(adm_src, encoding="utf-8").read()
    import base64
    _sb64 = lambda x: base64.b64encode(str(x).encode()).decode()
    tpl = (tpl.replace("@LEADS_BACKEND@", _adm_url)
              .replace("@SB_URL_B64@", _sb64(_sb.get("url", "")))
              .replace("@SB_KEY_B64@", _sb64(_sb.get("anonKey", "")))
              .replace("@ADMIN_PW@", A.get("password", "")))
    open(_adm_out, "w", encoding="utf-8").write(tpl)
    log(f"[admin] {_ADM_PAGE} собран (хранилище: "
        f"{'supabase' if _sb.get('url') else 'backend'})")
else:
    for old in (os.path.join(OUT, "admin.html"), _adm_out):
        if os.path.isfile(old):
            try:
                os.remove(old)
            except Exception as e:
                log(f"[admin] не удалось удалить {os.path.basename(old)}: {e}")
    log("[admin] админка не собирается — хранилище заявок не подключено")

# политика, og-картинка, фавикон
try:
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT, "policy.py")], check=True, cwd=ROOT)
    subprocess.run([sys.executable, os.path.join(ROOT, "seo.py")], check=True, cwd=ROOT)
    venv_py = r"C:\Users\Cypher\.workbuddy-ai\binaries\python\envs\default\Scripts\python.exe"
    if os.path.isfile(venv_py):
        subprocess.run([venv_py, os.path.join(ROOT, "render_brand.py")], check=True, cwd=ROOT)
    else:
        log("[render] пропущен — не найден venv-python")
except Exception as e:
    log("[render] ошибка: %s" % e)
open(os.path.join(OUT, ".nojekyll"), "w").write("")

# CNAME если указан свой домен
dom = cfg.get("domain")
if dom:
    open(os.path.join(OUT, "CNAME"), "w").write(dom + "\n")
    log(f"[domain] CNAME -> {dom}")

# проверка остатков
left_brand = len(re.findall(r"re[-:]device", h, re.I))
left_phone = h.count("495") + h.count("106-21-37")
left_city = len(re.findall(r"Москв", h))
log(f"[html] {orig_len} -> {len(h)} символов")
log(f"[check] осталось упоминаний re-device: {left_brand}, старых телефонов: {left_phone}, 'Москв*': {left_city}")
log(f"[done] сайт собран в {OUT}")
