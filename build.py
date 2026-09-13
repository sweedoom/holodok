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
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
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
            shutil.copytree(s, d)
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
h = h.replace("Цветной бул., 15, стр. 1", cfg["address"])
h = h.replace("с 9:00 до 21:00", cfg["workHours"])
h = h.replace("Mo-Su 09:00-21:00", cfg["openingHours"])
h = h.replace("55.779919", str(cfg["geo"]["lat"])).replace("37.601771", str(cfg["geo"]["lon"]))
h = h.replace('"ratingValue":"4.9"', '"ratingValue":"%s"' % cfg["rating"])
h = h.replace("738 оценок", "%s оценок" % cfg["reviews"])

# 8a. теглайн
h = h.replace("Сервисный центр в Москве", "%s в %s" % (cfg.get("tagline", "Сервисный центр"), C["prep"]))
h = h.replace(">в Москве<", ">в %s<" % C["prep"])

# 9. логотип
h = h.replace("public/images/logo/logo-header.png", cfg["logo"])

# 10. карта
if cfg.get("map", {}).get("mode") == "iframe":
    url = "https://yandex.ru/map-widget/v1/?ll={lon},{lat}&z=16&text={txt}".format(
        lon=cfg["geo"]["lon"], lat=cfg["geo"]["lat"],
        txt=(cfg["city"]["nom"] + " " + cfg["address"]).replace(" ", "%20"))
    h = re.sub(
        r'<div id="n1_[0-9a-z]+" style="display: inline-block; width: 100%; height: 441px;"></div>',
        f'<iframe src="{url}" width="100%" height="441" frameborder="0" '
        f'style="border:0;display:inline-block;width:100%;height:441px" loading="lazy"></iframe>', h)
    log("[map] режим iframe (без API-ключа)")
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
  function sendTG(d, L){
    var text = 'Заявка: ' + d.title + '\\nТелефон: ' + d.phone +
               (d.name ? '\\nИмя: ' + d.name : '') +
               (d.message ? '\\nСообщение: ' + d.message : '') +
               (d.promo ? '\\nПромо: ' + d.promo : '') + '\\nСтраница: ' + d.page;
    return fetch('https://api.telegram.org/bot' + L.telegramBotToken + '/sendMessage', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({chat_id: L.telegramChatId, text: text})
    });
  }
  jQuery(function($){
    $('form').off('submit').on('submit', function(e){
      e.preventDefault();
      var form = this, d = collect(form), L = window.SITE_LEADS;
      var digits = (d.phone.match(/\\d+/g) || []).join('');
      if (digits.length !== 11) { alert('Введите номер телефона полностью'); return false; }
      if (L.mode === 'telegram' && L.telegramBotToken && L.telegramChatId) {
        sendTG(d, L).then(function(){ ok(form); }).catch(function(){
          alert('Не удалось отправить. Позвоните нам или напишите на почту.');
        });
      } else if (L.mode === 'endpoint' && L.endpoint) {
        fetch(L.endpoint, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(d)})
          .then(function(){ ok(form); }).catch(function(){ alert('Ошибка отправки. Попробуйте позже.'); });
      } else {
        var body = encodeURIComponent('Телефон: ' + d.phone + (d.name ? ', Имя: ' + d.name : '') +
                   (d.message ? ', Сообщение: ' + d.message : '') + '\\nСтраница: ' + d.page);
        window.location.href = 'mailto:__EMAIL__?subject=' +
          encodeURIComponent(d.title) + '&body=' + body;
        ok(form);
      }
      return false;
    });
    // AJAX-подгрузка отзывов на статике не работает - прячем кнопку
    if (!$('#url-review').val().match(/^https?:/)) { $('.new-rev').hide(); }
  });
})();
</script>
"""
lead_js = lead_js.replace("__LEADS__", json.dumps({
    "mode": L.get("mode", "mailto"),
    "telegramBotToken": L.get("telegramBotToken", ""),
    "telegramChatId": L.get("telegramChatId", ""),
    "endpoint": L.get("endpoint", ""),
}, ensure_ascii=False)).replace("__EMAIL__", cfg["email"])

if head_add:
    h = h.replace("</head>", "".join(head_add) + "</head>")

# 12. ссылки на политику/согласие (были #) -> реальные страницы
h = re.sub(r'(<a[^>]*class="[^"]*politic[^"]*"[^>]*)href="#"', r'\1href="politika.html"', h)
h = re.sub(r'(<a[^>]*href="#")[^>]*>Политика конфиденциальности', r'\1>Политика конфиденциальности', h)
h = re.sub(r'href="#"[^>]*>Политика конфиденциальности', 'href="politika.html">Политика конфиденциальности', h)
h = re.sub(r'href="#"[^>]*>Соглашение[^<]*', 'href="soglasie.html">Соглашение', h)
# подстраховка на любые оставшиеся footer-ссылки по тексту
h = h.replace('<a class="text-14 white w-600" itemprop="url" href="#">Политика',
              '<a class="text-14 white w-600" itemprop="url" href="politika.html">Политика')
h = h.replace('<a class="text-14 white w-600" itemprop="url" href="#">Соглашение',
              '<a class="text-14 white w-600" itemprop="url" href="soglasie.html">Соглашение')

h = h.replace("</body>", lead_js + "</body>")

# ------------------------------------------------------------------ запись
copy_assets()
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
make_logo(os.path.join(OUT, cfg["logo"].replace("/", os.sep)))
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(h)

# политика, og-картинка, фавикон
try:
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT, "policy.py")], check=True, cwd=ROOT)
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
