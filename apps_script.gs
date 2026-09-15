/**
 * ============================================================
 *  БЭКЕНД ЗАЯВОК — Google Apps Script
 *  ХОЛОД-ОК / ремонт парогенераторов Tylo
 * ============================================================
 *
 *  ЧТО ДЕЛАЕТ:
 *   1. Принимает заявку с сайта (POST)  -> пишет в Google Таблицу
 *   2. Отправляет заявку в Telegram    -> токен лежит ЗДЕСЬ, на сервере
 *   3. Отдаёт список заявок админке    -> только по паролю
 *
 *  ПОЧЕМУ ТАК:
 *   - токен бота НИКОГДА не попадает в код сайта и в админку
 *   - администратор веб-админки не видит и не может узнать про Telegram
 *   - заявки лежат в Google Таблице — их удобно смотреть и выгружать
 *
 * ------------------------------------------------------------
 *  УСТАНОВКА (5 минут, один раз):
 *   1. Создай новую Google Таблицу: https://sheets.new
 *   2. В меню: Расширения -> Apps Script
 *   3. Удали всё, вставь этот файл целиком
 *   4. Вверху выбери функцию setup и нажми "Выполнить"
 *      (первый раз попросит разрешения — разреши)
 *   5. Замени в setup() три значения: TG_TOKEN, TG_CHAT, ADMIN_PW
 *      и снова нажми "Выполнить"
 *   6. Наверху справа: "На развёртывание" -> "Новое развёртывание"
 *      Тип: Веб-приложение
 *      Выполнять как: Я
 *      У кого есть доступ: Все  (обязательно!)
 *      -> "На развёртывание" -> скопируй URL вида https://script.google.com/macros/s/...../exec
 *   7. Этот URL вставь в config.json -> admin.backendUrl
 *      и запусти: python build.py && bash deploy.sh
 * ============================================================
 */

// ---- ПЕРВОНАЧАЛЬНАЯ НАСТРОЙКА: запустить один раз ----
function setup() {
  PropertiesService.getScriptProperties().setProperties({
    TG_TOKEN: 'ВСТАВИТЬ_ТОКЕН_БОТА',
    TG_CHAT:  '8723283117',
    ADMIN_PW: 'придумай_пароль_админки'
  }, true);
  ensureHeaders();
  Logger.log('Готово. Теперь сделай развёртывание (Deploy -> New deployment).');
}

// ---------- таблица ----------
var SHEET_NAME = 'Заявки';
var HEADERS = ['Дата', 'ID', 'Имя', 'Телефон', 'Сообщение', 'Источник', 'Страница', 'Статус', 'Комментарий', 'UTM'];

function sheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#00966D').setFontColor('#ffffff');
    sh.setFrozenRows(1);
  }
  return sh;
}

function ensureHeaders() {
  var sh = sheet();
  if (sh.getLastRow() === 0) {
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#00966D').setFontColor('#ffffff');
    sh.setFrozenRows(1);
  }
}

// ---------- приём заявки с сайта ----------
function doPost(e) {
  try {
    var raw = e.postData && e.postData.contents ? e.postData.contents : '{}';
    var d = JSON.parse(raw);

    var phone = String(d.phone || '').trim();
    if (!phone) return out({ ok: false, error: 'no phone' });

    var id = Utilities.getUuid().substring(0, 8);
    var now = new Date();
    var row = [
      Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm:ss'),
      id,
      String(d.name || '').trim(),
      phone,
      String(d.message || '').trim(),
      String(d.title || 'Заявка с сайта').trim(),
      String(d.page || '').trim(),
      'new',
      '',
      String(d.utm || '').trim()
    ];

    sheet().appendRow(row);

    // ---- отправка в Telegram (токен только здесь) ----
    try {
      var p = PropertiesService.getScriptProperties();
      var token = p.getProperty('TG_TOKEN');
      var chat = p.getProperty('TG_CHAT');
      if (token && chat && token.indexOf('ВСТАВИТЬ') === -1) {
        UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
          method: 'post',
          contentType: 'application/json',
          payload: JSON.stringify({
            chat_id: chat,
            text: formatLead(row),
            parse_mode: 'HTML',
            disable_web_page_preview: true
          }),
          muteHttpExceptions: true
        });
      }
    } catch (tgErr) {
      Logger.log('Telegram error: ' + tgErr);
    }

    return out({ ok: true, id: id });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

function formatLead(r) {
  return '<b>\uD83D\uDD27 Новая заявка #' + r[1] + '</b>\n' +
         '<b>Источник:</b> ' + esc(r[5]) + '\n' +
         (r[2] ? '<b>Имя:</b> ' + esc(r[2]) + '\n' : '') +
         '<b>Телефон:</b> <code>' + esc(r[3]) + '</code>\n' +
         (r[4] ? '<b>Сообщение:</b> ' + esc(r[4]) + '\n' : '') +
         (r[6] ? '<b>Страница:</b> ' + esc(r[6]) + '\n' : '') +
         '<b>Время:</b> ' + r[0];
}

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ---------- отдача данных в админку ----------
function doGet(e) {
  var p = e.parameter || {};
  var action = p.action || 'ping';

  if (action === 'ping') return out({ ok: true, service: 'leads' });

  // всё остальное — только по паролю
  var pw = PropertiesService.getScriptProperties().getProperty('ADMIN_PW');
  if (!pw || p.pw !== pw) return out({ ok: false, error: 'Неверный пароль' });

  try {
    if (action === 'list')    return out({ ok: true, leads: readAll() });
    if (action === 'status')  return out({ ok: true, done: setField(p.id, 8, p.value) });
    if (action === 'comment') return out({ ok: true, done: setField(p.id, 9, p.value) });
    if (action === 'delete')  return out({ ok: true, done: deleteRow(p.id) });
    return out({ ok: false, error: 'unknown action' });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

function readAll() {
  var sh = sheet();
  var last = sh.getLastRow();
  if (last < 2) return [];
  var data = sh.getRange(2, 1, last - 1, HEADERS.length).getValues();
  var leads = [];
  for (var i = 0; i < data.length; i++) {
    leads.push({
      date: data[i][0], id: data[i][1], name: data[i][2], phone: data[i][3],
      message: data[i][4], source: data[i][5], page: data[i][6],
      status: data[i][7] || 'new', comment: data[i][8] || '', utm: data[i][9] || ''
    });
  }
  return leads.reverse(); // свежие сверху
}

function setField(id, col, value) {
  var sh = sheet();
  var ids = sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (String(ids[i][0]) === String(id)) {
      sh.getRange(i + 2, col).setValue(value);
      return true;
    }
  }
  return false;
}

function deleteRow(id) {
  var sh = sheet();
  var ids = sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (String(ids[i][0]) === String(id)) {
      sh.deleteRow(i + 2);
      return true;
    }
  }
  return false;
}

// ---------- ответ (поддерживаем и CORS, и JSONP) ----------
function out(obj) {
  var cb = (typeof e !== 'undefined' && e && e.parameter) ? e.parameter.callback : null;
  var body = JSON.stringify(obj);
  if (cb) {
    return ContentService.createTextOutput(cb + '(' + body + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(body).setMimeType(ContentService.MimeType.JSON);
}
