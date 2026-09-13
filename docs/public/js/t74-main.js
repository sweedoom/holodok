/**
 * Правки 20.08.2026 (ТЗ главная): поведение новых секций главной страницы.
 *
 * Табы географии, аккордеон FAQ, раскрытие брендов и SEO-текста,
 * попап с условиями гарантии, промо-код в форму заявки, слайдеры.
 *
 * Без зависимостей, кроме Swiper для слайдеров — он уже подключён в base.php.
 */
(function () {
  "use strict";

  var onReady = function (fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  };

  // Дребезг для resize-обработчиков
  function debounce(fn, wait) {
    var timer = null;
    return function () {
      var args = arguments,
        ctx = this;
      clearTimeout(timer);
      timer = setTimeout(function () {
        fn.apply(ctx, args);
      }, wait || 150);
    };
  }

  /**
   * Цель в Яндекс.Метрику. Номер счётчика берём из скрытого поля,
   * а если его на странице нет — из уже инициализированного счётчика.
   * Молча выходим, если Метрики нет: аналитика не должна ронять интерфейс.
   */
  function reachGoal(goal) {
    if (!goal || typeof window.ym !== "function") return;

    var id = null;
    var field = document.getElementById("metrika-ajax-form");
    if (field && field.value) {
      id = field.value;
    } else if (window.Ya && window.Ya._metrika && window.Ya._metrika.counters) {
      var keys = Object.keys(window.Ya._metrika.counters);
      if (keys.length) id = keys[0].replace(/\D/g, "");
    }
    if (!id) return;

    try {
      window.ym(id, "reachGoal", goal);
    } catch (e) {
      /* аналитика не критична */
    }
  }

  // ---------------------------------------------------------------- Табы
  // Содержимое всех табов лежит в HTML, неактивные скрыты через hidden.
  // Переключение без перезагрузки и без AJAX.
  function initTabs(root) {
    var head = root.querySelector(".t74-tabs__head");
    var body = root.querySelector(".t74-tabs__body");
    if (!head || !body) return;

    var tabs = Array.prototype.slice.call(head.querySelectorAll('[role="tab"]'));
    var panels = Array.prototype.slice.call(body.querySelectorAll('[role="tabpanel"]'));
    if (!tabs.length) return;

    // Высота контейнера не должна прыгать при переключении:
    // меряем самый длинный таб и фиксируем min-height.
    function lockHeight() {
      if (window.innerWidth < 830) {
        body.style.minHeight = "";
        return;
      }
      var max = 0;
      panels.forEach(function (panel) {
        var wasHidden = panel.hasAttribute("hidden");
        if (wasHidden) {
          panel.style.visibility = "hidden";
          panel.style.position = "absolute";
          panel.removeAttribute("hidden");
        }
        max = Math.max(max, panel.offsetHeight);
        if (wasHidden) {
          panel.setAttribute("hidden", "");
          panel.style.visibility = "";
          panel.style.position = "";
        }
      });
      body.style.minHeight = max ? max + "px" : "";
    }

    // На мобильных ряд табов скроллится — активный подтягиваем в видимую область.
    // Считаем через getBoundingClientRect, а не offsetLeft: у ряда табов
    // position: static, и offsetLeft мерялся бы от чужого предка.
    function scrollTabIntoView(tab) {
      if (head.scrollWidth <= head.clientWidth) return;
      var headRect = head.getBoundingClientRect();
      var tabRect = tab.getBoundingClientRect();
      var delta = tabRect.left - headRect.left - (head.clientWidth - tabRect.width) / 2;
      var max = head.scrollWidth - head.clientWidth;
      head.scrollLeft = Math.max(0, Math.min(head.scrollLeft + delta, max));
    }

    function activate(index, setFocus) {
      tabs.forEach(function (tab, i) {
        var active = i === index;
        tab.classList.toggle("is-active", active);
        tab.setAttribute("aria-selected", active ? "true" : "false");
        tab.setAttribute("tabindex", active ? "0" : "-1");
      });
      panels.forEach(function (panel, i) {
        if (i === index) {
          panel.removeAttribute("hidden");
        } else {
          panel.setAttribute("hidden", "");
        }
      });
      scrollTabIntoView(tabs[index]);
      if (setFocus) tabs[index].focus();
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () {
        activate(i, false);
        reachGoal(tab.getAttribute("data-geo-goal"));
      });

      // Переключение с клавиатуры стрелками, Home/End — к краям.
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") next = (i + 1) % tabs.length;
        else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = (i - 1 + tabs.length) % tabs.length;
        else if (e.key === "Home") next = 0;
        else if (e.key === "End") next = tabs.length - 1;
        if (next === null) return;
        e.preventDefault();
        activate(next, true);
        reachGoal(tabs[next].getAttribute("data-geo-goal"));
      });
    });

    lockHeight();
    scrollTabIntoView(tabs[0]);
    window.addEventListener("resize", debounce(lockHeight, 200));
    // Шрифты догружаются позже вёрстки и меняют высоту панелей.
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(lockHeight);
    }
    window.addEventListener("load", lockHeight);
  }

  // ------------------------------------------------- Кнопки «показать всё»
  // Переключают класс is-hidden у скрытых элементов и подпись кнопки.
  /**
   * Правки 03.09.2026 (правки заказчика, п.18): при сворачивании список
   * оказывался пустым.
   *
   * Было: items — ВСЕ элементы секции, и на сворачивании is-hidden вешался
   * в том числе на первые 12, которые видны с самого начала. Раскрыл список,
   * свернул обратно — на месте брендов пусто.
   *
   * Стало: запоминаем на старте только те элементы, что и так были скрыты
   * (PHP помечает их классом is-hidden при выводе), и дальше переключаем
   * ровно их. Первые 12 остаются на экране всегда.
   */
  function initToggleList(button, itemsSelector) {
    if (!button) return;
    var container = button.closest("section");
    if (!container) return;
    var items = Array.prototype.filter.call(
      container.querySelectorAll(itemsSelector),
      function (item) {
        return item.classList.contains("is-hidden");
      }
    );
    if (!items.length) return;

    button.addEventListener("click", function () {
      var expanded = button.classList.toggle("is-expanded");
      items.forEach(function (item) {
        item.classList.toggle("is-hidden", !expanded);
      });
      button.textContent = expanded
        ? button.getAttribute("data-less")
        : button.getAttribute("data-more");
    });
  }

  // ------------------------------------------------------------- Аккордеон
  // При загрузке все пункты закрыты. Открытие — по клику, высота анимируется.
  function initFaq() {
    var items = document.querySelectorAll(".t74-faq__item");
    Array.prototype.forEach.call(items, function (item) {
      var question = item.querySelector(".t74-faq__q");
      var answer = item.querySelector(".t74-faq__a");
      if (!question || !answer) return;

      question.addEventListener("click", function () {
        var open = item.classList.toggle("is-open");
        question.setAttribute("aria-expanded", open ? "true" : "false");
        answer.style.maxHeight = open ? answer.scrollHeight + "px" : "";
      });

      // На странице бренда первый вопрос раскрыт разметкой (ТЗ п.21.3):
      // без этого CSS-переход стартовал бы с нулевой высоты и ответ не виден.
      if (item.classList.contains("is-open")) {
        answer.style.maxHeight = answer.scrollHeight + "px";
      }
    });

    // Пересчёт высоты открытых ответов при смене ширины экрана
    window.addEventListener(
      "resize",
      debounce(function () {
        Array.prototype.forEach.call(items, function (item) {
          if (!item.classList.contains("is-open")) return;
          var answer = item.querySelector(".t74-faq__a");
          if (answer) answer.style.maxHeight = answer.scrollHeight + "px";
        });
      }, 200)
    );
  }


  // ------------------------------- Неисправности: аккордеон строк (ТЗ п.6.2)
  /**
   * Раскрытие по клику в любое место строки, кроме кнопки «Вызвать мастера».
   * Одновременно может быть раскрыто несколько строк, в том числе в обеих
   * колонках: колонки — независимые потоки, поэтому строка слева не двигает
   * правую. Первая строка страницы раскрыта разметкой — ей высоту выставляем
   * на старте, иначе CSS-переход стартует с max-height: 0.
   */
  function initFaults() {
    var items = document.querySelectorAll(".t74-fault");
    if (!items.length) return;

    function setHeight(item) {
      var body = item.querySelector(".t74-fault__body");
      if (!body) return;
      body.style.maxHeight = item.classList.contains("is-open") ? body.scrollHeight + "px" : "";
    }

    Array.prototype.forEach.call(items, function (item) {
      var head = item.querySelector(".t74-fault__head");
      if (!head) return;

      function toggle() {
        var open = item.classList.toggle("is-open");
        head.setAttribute("aria-expanded", open ? "true" : "false");
        setHeight(item);
      }

      head.addEventListener("click", function (e) {
        // Кнопка заявки открывает форму и строку не трогает
        if (e.target.closest(".t74-fault__btn")) return;
        toggle();
      });

      head.addEventListener("keydown", function (e) {
        if (e.key !== "Enter" && e.key !== " " && e.key !== "Spacebar") return;
        if (e.target.closest(".t74-fault__btn")) return;
        e.preventDefault();
        toggle();
      });

      setHeight(item);
    });

    // Ширина колонки меняется — меняется и высота раскрытого текста
    window.addEventListener(
      "resize",
      debounce(function () {
        Array.prototype.forEach.call(items, setHeight);
      }, 200)
    );
  }

  // ------------------------- Прайс: раскрытие описания услуги (ТЗ п.4.4)
  /**
   * Описание лежит в строке целиком и обрезано многоточием через CSS.
   * Клик по строке раскрывает его; клик по названию услуги и по кнопке
   * «Заказать» остаётся переходом по ссылке, а не раскрытием.
   */
  function initPriceDesc() {
    var rows = document.querySelectorAll(".price-table-item.t74-has-desc");
    Array.prototype.forEach.call(rows, function (row) {
      row.addEventListener("click", function (e) {
        if (e.target.closest("a") || e.target.closest("button")) return;
        row.classList.toggle("is-open");
      });
    });
  }

  // ------------------------------------------------------ Лайтбокс сканов
  /**
   * Правки 03.09.2026 (правки заказчика, п.11): просмотр сертификатов.
   *
   * Миниатюра в ленте — <button> с data-t74-lightbox-src, клик открывает скан
   * в полный размер. Стрелки листают ленту, Esc и клик по фону закрывают.
   * Своей разметки в HTML не держим: оверлей собирается здесь один на страницу.
   */
  function initLightbox() {
    var strips = document.querySelectorAll("[data-t74-lightbox]");
    if (!strips.length) return;

    var items = [];
    Array.prototype.forEach.call(strips, function (strip) {
      Array.prototype.forEach.call(
        strip.querySelectorAll("[data-t74-lightbox-src]"),
        function (btn) {
          items.push(btn);
        }
      );
    });
    if (!items.length) return;

    var box = document.createElement("div");
    box.className = "t74-lightbox";
    box.setAttribute("hidden", "");
    box.innerHTML =
      '<div class="t74-lightbox__backdrop" data-close></div>' +
      '<div class="t74-lightbox__inner" role="dialog" aria-modal="true">' +
      '<button type="button" class="t74-lightbox__close" data-close aria-label="Закрыть">&times;</button>' +
      '<button type="button" class="t74-lightbox__nav t74-lightbox__prev" aria-label="Предыдущий документ">&#8249;</button>' +
      '<img class="t74-lightbox__img" src="" alt="">' +
      '<button type="button" class="t74-lightbox__nav t74-lightbox__next" aria-label="Следующий документ">&#8250;</button>' +
      '<div class="t74-lightbox__caption"></div>' +
      "</div>";
    document.body.appendChild(box);

    var img = box.querySelector(".t74-lightbox__img");
    var caption = box.querySelector(".t74-lightbox__caption");
    var current = 0;
    var lastFocused = null;

    function show(index) {
      current = (index + items.length) % items.length;
      var btn = items[current];
      var text = btn.getAttribute("data-t74-lightbox-caption") || "";
      img.src = btn.getAttribute("data-t74-lightbox-src");
      img.alt = text;
      caption.textContent = text;
      caption.hidden = text === "";
    }

    function open(index) {
      lastFocused = document.activeElement;
      show(index);
      box.removeAttribute("hidden");
      document.body.classList.add("t74-modal-open");
      box.querySelector(".t74-lightbox__close").focus();
    }

    function close() {
      box.setAttribute("hidden", "");
      document.body.classList.remove("t74-modal-open");
      img.src = "";
      if (lastFocused) lastFocused.focus();
    }

    items.forEach(function (btn, i) {
      btn.addEventListener("click", function () {
        open(i);
      });
    });

    // Одна кнопка листает — прячем стрелки, если документ всего один
    if (items.length < 2) {
      Array.prototype.forEach.call(box.querySelectorAll(".t74-lightbox__nav"), function (nav) {
        nav.hidden = true;
      });
    }

    box.querySelector(".t74-lightbox__prev").addEventListener("click", function () {
      show(current - 1);
    });
    box.querySelector(".t74-lightbox__next").addEventListener("click", function () {
      show(current + 1);
    });
    Array.prototype.forEach.call(box.querySelectorAll("[data-close]"), function (el) {
      el.addEventListener("click", close);
    });
    document.addEventListener("keydown", function (e) {
      if (box.hasAttribute("hidden")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
  }

  // ------------------------------------------------- Попап условий гарантии
  function initWarrantyModal() {
    var modal = document.getElementById("t74-warranty");
    if (!modal) return;
    var lastFocused = null;

    function open() {
      lastFocused = document.activeElement;
      modal.removeAttribute("hidden");
      document.body.classList.add("t74-modal-open");
      var closeBtn = modal.querySelector(".t74-modal__close");
      if (closeBtn) closeBtn.focus();
    }

    function close() {
      modal.setAttribute("hidden", "");
      document.body.classList.remove("t74-modal-open");
      if (lastFocused) lastFocused.focus();
    }

    Array.prototype.forEach.call(document.querySelectorAll(".t74-warranty-open"), function (btn) {
      btn.addEventListener("click", open);
    });
    Array.prototype.forEach.call(modal.querySelectorAll("[data-t74-close]"), function (el) {
      el.addEventListener("click", close);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !modal.hasAttribute("hidden")) close();
    });
  }

  // ------------------------------------------------------- SEO-текст
  // На главной блок один, на странице бренда их два (ТЗ п.16) —
  // поэтому обходим все кнопки и ищем текст в своей же обёртке.
  function initSeoToggle() {
    var buttons = document.querySelectorAll(".t74-seo__toggle");
    Array.prototype.forEach.call(buttons, function (button) {
      var scope = button.closest(".t74-seo__block") || button.closest("section");
      var body = scope ? scope.querySelector(".t74-seo__body") : null;
      if (!body) return;

      button.addEventListener("click", function () {
        var collapsed = body.classList.toggle("is-collapsed");
        button.textContent = collapsed
          ? button.getAttribute("data-more")
          : button.getAttribute("data-less");
        if (collapsed) {
          // Возвращаем пользователя к началу блока, иначе он окажется
          // где-то в середине схлопнувшегося текста.
          var top = body.getBoundingClientRect().top + window.pageYOffset - 100;
          window.scrollTo({ top: top, behavior: "smooth" });
        }
      });
    });
  }

  // ------------------------------------------------------------ Промо-код
  // Кнопка акции открывает общую форму заявки и кладёт в неё скрытый промо-код.
  // Любая другая кнопка, открывающая ту же форму, промо-код очищает,
  // чтобы он не утёк в следующую заявку.
  function initPromo() {
    var field = document.getElementById("t74-promo-field");
    var titleField = document.getElementById("t74-promo-title");
    var titleNode = document.querySelector(".modal_get .modal__title");
    if (!field) return;

    var defaultTitle = titleNode ? titleNode.textContent : "";

    document.addEventListener(
      "click",
      function (e) {
        var trigger = e.target.closest ? e.target.closest(".open-popup") : null;
        if (!trigger) return;

        var promo = trigger.getAttribute("data-promo") || "";
        // Правки 30.08.2026: заголовок формы задают и кнопки без промо-кода —
        // «Вызвать мастера» в строке неисправности передаёт в заявку
        // название поломки (ТЗ п.6.2).
        var formTitle = trigger.getAttribute("data-promo-title") || "";
        field.value = promo;

        if (titleField) {
          titleField.value = formTitle;
        }
        if (titleNode) {
          titleNode.textContent = formTitle || defaultTitle;
        }
      },
      true
    );
  }

  // -------------------------------------------------------------- Слайдеры
  function initSliders() {
    if (typeof window.Swiper !== "function") return;

    if (document.querySelector(".t74-prices__slider")) {
      new window.Swiper(".t74-prices__slider", {
        slidesPerView: 1,
        spaceBetween: 20,
        grabCursor: true,
        navigation: {
          nextEl: ".t74-prices__next",
          prevEl: ".t74-prices__prev",
        },
        pagination: {
          el: ".t74-prices__pagination",
          clickable: true,
        },
        breakpoints: {
          650: { slidesPerView: 2, spaceBetween: 20 },
          1050: { slidesPerView: 3, spaceBetween: 24 },
        },
      });
    }

    if (document.querySelector(".t74-masters__slider")) {
      new window.Swiper(".t74-masters__slider", {
        slidesPerView: 1,
        spaceBetween: 20,
        grabCursor: true,
        navigation: {
          nextEl: ".t74-masters__next",
          prevEl: ".t74-masters__prev",
        },
        pagination: {
          el: ".t74-masters__pagination",
          clickable: true,
        },
        breakpoints: {
          650: { slidesPerView: 2, spaceBetween: 20 },
          1050: { slidesPerView: 3, spaceBetween: 24 },
          1200: { slidesPerView: 4, spaceBetween: 24 },
        },
      });
    }
  }

  // ------------------------------ «Мы ремонтируем»: кнопка «Показать больше»
  /**
   * Правки 27.08.2026. Сама механика кнопки — в mainScript.js: она снимает и
   * возвращает класс .no_show_card, а прячет карточки CSS (t74-main.css).
   * Здесь только одно: убрать кнопку, если прятать нечего.
   *
   * Сколько карточек влезает в два ряда, зависит от ширины экрана
   * (12 / 6 / 4 — те же брейкпоинты, что и в CSS), поэтому пересчитываем
   * на resize. Если кнопку успели нажать, список уже раскрыт — не трогаем.
   */
  function initCatalogMore() {
    var wrap = document.querySelector(".catalog .show-cat-card");
    var grid = document.querySelector(".catalog .catalog-cards");
    if (!wrap || !grid) return;

    var total = grid.querySelectorAll(".cards-item").length;

    function visibleLimit() {
      if (window.innerWidth <= 830) return 4;
      if (window.innerWidth <= 1050) return 6;
      return 12;
    }

    function sync() {
      wrap.classList.toggle(
        "t74-is-hidden",
        grid.classList.contains("no_show_card") && total <= visibleLimit()
      );
    }

    sync();
    window.addEventListener("resize", debounce(sync, 150));
  }

  onReady(function () {
    Array.prototype.forEach.call(document.querySelectorAll("[data-t74-tabs]"), initTabs);

    initToggleList(document.querySelector(".t74-brands__more"), ".t74-brands__item");
    initToggleList(document.querySelector(".t74-faq__more"), ".t74-faq__item");
    // Сетка моделей бренда на странице модели (ТЗ модели, п.6.2)
    initToggleList(document.querySelector(".t74-models__more"), ".t74-models__item");

    initCatalogMore();
    initFaults();
    initPriceDesc();
    initFaq();
    initLightbox();
    initWarrantyModal();
    initSeoToggle();
    initPromo();
    initSliders();
  });
})();
