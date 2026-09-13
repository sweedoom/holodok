



//menu

let menuOpen = document.querySelectorAll(".burger-menu");
let menuClose = document.querySelectorAll(".menu-close");
let menu = document.querySelectorAll(".menu");

menu[0].style.top = "-100%";
//menu[1].style.bottom = "-100%";

menuOpen.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.classList[0] == "top") {
      menu[0].classList.add("active");
      menu[0].style.top = "0%";
    } else if (button.classList[0] == "bottom") {
      menu[1].classList.add("active");
      menu[1].style.bottom = "0%";
    }
    const body = document.body;
    body.style.overflowY = "hidden";
  });
});
menuClose.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.classList[0] == "top") {
      menu[0].classList.remove("active");
      menu[0].style.top = "-100%";
    } else if (button.classList[0] == "bottom") {
      menu[1].classList.remove("active");
      menu[1].style.bottom = "-100%";
    }
    const body = document.body;
    body.style.overflowY = "";
  });
});

//menu

// modals
let openPopupButtons = document.querySelectorAll(".open-popup");
// let popupBgForm = document.querySelector(".popup-form");
let popupBg = document.querySelector(".overlay");
let popup = document.querySelector(".modal");

openPopupButtons.forEach((button) => {
  // Перебираем все кнопки
  button.addEventListener("click", (e) => {
    // Для каждой вешаем обработчик событий на клик
    e.preventDefault(); // Предотвращаем дефолтное поведение браузера

    console.log(popupBg.classList);
    popupBg.classList.add("overlay_active"); // Добавляем класс 'active' для фона
    popup.classList.add("modal_active"); // И для самого окна
    menu.forEach((e) => {
      e.classList.remove("active");
    });
    const body = document.body;
    body.style.overflowY = "hidden";

  });
});

// modals


// input close / checker

// Переменные для формы с текстом "Остались вопросы?"

var nameInput = document.getElementById('name');
var phoneInput = document.getElementById('phone');
var nameError = document.getElementById('name-error');
var phoneError = document.getElementById('phone-error');
var formBtn = document.querySelectorAll(".form-btn")
var quesForm = document.getElementById('ques')

// Переменные для формы с текстом "Остались вопросы?"

// код первой формы с текстом "Остались вопросы?"

if (quesForm === null) {

} else {
  document.getElementById('ques').addEventListener('submit', function (event) {

    var valid = true;
    console.log(phoneInput.value.length);
    if (nameInput.value.length < 3) {
      nameInput.classList.add('error');
      nameError.innerText = 'Произошла ошибка';
      valid = false;
    } else {
      nameInput.classList.add('success');
      nameError.classList.add('success');
      nameError.innerText = 'Поле заполнено верно';
    }

    if (phoneInput.value.length < 17) {
      phoneInput.classList.add('error');
      phoneError.innerText = 'Произошла ошибка';
      valid = false;
    } else {
      phoneInput.classList.add('success');
      phoneError.classList.add('success');
      phoneError.innerText = 'Поле заполнено верно';
    }

    if (!valid) {
      event.preventDefault();
    } else {
      event.preventDefault();

      setTimeout(function () {
        nameInput.value = '';
        phoneInput.value = '';
        phoneError.innerText = '';
        nameError.innerText = '';
        phoneInput.classList.remove('success');
        nameInput.classList.remove('success');
        phoneInput.classList.remove('error');
        nameInput.classList.remove('error');
        formBtn.forEach((e) => {
          e.blur();
        })
      }, 3000);

    }
  });
}





const searchInputName = document.querySelectorAll(".white-inp-name");
function clearName() {
  searchInputName.forEach((el) => {
    el.value = '';
    nameInput.classList.remove('error');
    nameInput.classList.remove('success');
    nameError.classList.remove('error');
    nameError.classList.remove('success');
    nameError.innerText = '';
  })

}
const searchInputPhone = document.querySelectorAll(".white-inp-phone");
function clearPhone() {
  searchInputPhone.forEach((el) => {
    el.value = '';
    phoneInput.classList.remove('error');
    phoneInput.classList.remove('success');
    phoneError.classList.remove('error');
    phoneError.classList.remove('success');
    phoneError.innerText = '';
  })
}
// код первой формы с текстом "Остались вопросы?"

// -----------------------// -----------------------// -----------------------// -----------------------

// Переменные для главной формы Баннер

var nameInputMain = document.getElementById('name-main');
var phoneInputMain = document.getElementById('phone-main');
var nameErrorMain = document.getElementById('name-error-main');
var phoneErrorMain = document.getElementById('phone-error-main');
var formBtn = document.querySelectorAll(".form-btn")
var quesFormMain = document.getElementById("ques-main")

// Переменные для главной формы Баннер

// код главной формы Баннер
if (quesFormMain === null) {

} else {
  document.getElementById('ques-main').addEventListener('submit', function (event) {

    var valid = true;
    // console.log(phoneInputMain.value.length);
    if (nameInputMain.value.length < 3) {
      nameInputMain.classList.add('error');
      nameErrorMain.innerText = 'Произошла ошибка';
      valid = false;
    } else {
      nameInputMain.classList.add('success');
      nameErrorMain.classList.add('success');
      nameErrorMain.innerText = 'Поле заполнено верно';
    }

    if (phoneInputMain.value.length < 17) {
      phoneInputMain.classList.add('error');
      phoneErrorMain.innerText = 'Произошла ошибка';
      valid = false;
    } else {
      phoneInputMain.classList.add('success');
      phoneErrorMain.classList.add('success');
      phoneErrorMain.innerText = 'Поле заполнено верно';
    }

    if (!valid) {
      event.preventDefault();
    } else {
      event.preventDefault();

      setTimeout(function () {
        nameInputMain.value = '';
        phoneInputMain.value = '';
        phoneErrorMain.innerText = '';
        nameErrorMain.innerText = '';
        nameErrorMain.classList.remove('success');
        phoneErrorMain.classList.remove('error');
        phoneErrorMain.classList.remove('success');
        nameErrorMain.classList.remove('error');
        phoneInputMain.classList.remove('success');
        nameInputMain.classList.remove('success');
        phoneInputMain.classList.remove('error');
        nameInputMain.classList.remove('error');

        formBtn.forEach((e) => {
          e.blur();
        })
      }, 3000);

    }
  });
}




const searchInputNameMain = document.querySelectorAll(".white-inp-name-main");
function clearNameMain() {
  nameInputMain.value = '';
  nameInputMain.classList.remove('error');
  nameInputMain.classList.remove('success');
  nameErrorMain.classList.remove('error');
  nameErrorMain.classList.remove('success');
  nameErrorMain.innerText = '';

}
const searchInputPhoneMain = document.querySelectorAll(".white-inp-phone-main");
function clearPhoneMain() {
  phoneInputMain.value = '';
  phoneInputMain.classList.remove('error');
  phoneInputMain.classList.remove('success');
  phoneErrorMain.classList.remove('error');
  phoneErrorMain.classList.remove('success');
  phoneErrorMain.innerText = '';
}
// код главной формы Баннер

// -----------------------// -----------------------// -----------------------// -----------------------

// Переменные для главной формы Попап

var nameInputPop = document.getElementById('name-Pop');
var phoneInputPop = document.getElementById('phone-Pop');
var nameErrorPop = document.getElementById('name-error-Pop');
var phoneErrorPop = document.getElementById('phone-error-Pop');
var formBtn = document.querySelectorAll(".form-btn")

// Переменные для главной формы Попап

// код главной формы Попап
document.getElementById('ques-Pop').addEventListener('submit', function (event) {

  var valid = true;
  console.log(phoneInputPop.value.length);
  if (nameInputPop.value.length < 3) {
    nameInputPop.classList.add('error');
    nameErrorPop.innerText = 'Произошла ошибка';
    valid = false;
  } else {
    nameInputPop.classList.add('success');
    nameErrorPop.classList.add('success');
    nameErrorPop.innerText = 'Поле заполнено верно';
  }

  if (phoneInputPop.value.length < 17) {
    phoneInputPop.classList.add('error');
    phoneErrorPop.innerText = 'Произошла ошибка';
    valid = false;
  } else {
    phoneInputPop.classList.add('success');
    phoneErrorPop.classList.add('success');
    phoneErrorPop.innerText = 'Поле заполнено верно';
  }

  if (!valid) {
    event.preventDefault();
  } else {
    event.preventDefault();

    setTimeout(function () {
      nameInputPop.value = '';
      phoneInputPop.value = '';
      phoneErrorPop.innerText = '';
      nameErrorPop.innerText = '';
      nameErrorPop.classList.remove('success');
      phoneErrorPop.classList.remove('error');
      phoneErrorPop.classList.remove('success');
      nameErrorPop.classList.remove('error');
      phoneInputPop.classList.remove('success');
      nameInputPop.classList.remove('success');
      phoneInputPop.classList.remove('error');
      nameInputPop.classList.remove('error');

      formBtn.forEach((e) => {
        e.blur();
      })
    }, 3000);

  }
});



const searchInputNamePop = document.querySelectorAll(".white-inp-name-Pop");
function clearNamePop() {
  nameInputPop.value = '';
  nameInputPop.classList.remove('error');
  nameInputPop.classList.remove('success');
  nameErrorPop.classList.remove('error');
  nameErrorPop.classList.remove('success');
  nameErrorPop.innerText = '';

}
const searchInputPhonePop = document.querySelectorAll(".white-inp-phone-Pop");
function clearPhonePop() {
  phoneInputPop.value = '';
  phoneInputPop.classList.remove('error');
  phoneInputPop.classList.remove('success');
  phoneErrorPop.classList.remove('error');
  phoneErrorPop.classList.remove('success');
  phoneErrorPop.innerText = '';
}
// код главной формы Попап

// -----------------------// -----------------------// -----------------------// -----------------------

// Переменные для главной формы с текстом "Скидка"

var nameInputSale = document.getElementById('name-Sale');
var phoneInputSale = document.getElementById('phone-Sale');
var nameErrorSale = document.getElementById('name-error-Sale');
var phoneErrorSale = document.getElementById('phone-error-Sale');
var formBtn = document.querySelectorAll(".form-btn")
var saleForm = document.getElementById('ques-Sale');

// Переменные для главной формы с текстом "Скидка"
// код главной формы с текстом "Скидка"
if (saleForm === null) {

} else {
  document.getElementById('ques-Sale').addEventListener('submit', function (event) {

    var valid = true;
    console.log(phoneInputSale.value.length);
    if (nameInputSale.value.length < 3) {
      nameInputSale.classList.add('error');
      nameErrorSale.innerText = 'Произошла ошибка';
      valid = false;
    } else {
      nameInputSale.classList.add('success');
      nameErrorSale.classList.add('success');
      nameErrorSale.innerText = 'Поле заполнено верно';
    }

    if (phoneInputSale.value.length < 17) {
      phoneInputSale.classList.add('error');
      phoneErrorSale.innerText = 'Произошла ошибка';
      valid = false;
    } else {
      phoneInputSale.classList.add('success');
      phoneErrorSale.classList.add('success');
      phoneErrorSale.innerText = 'Поле заполнено верно';
    }

    if (!valid) {
      event.preventDefault();
    } else {
      event.preventDefault();

      setTimeout(function () {
        nameInputSale.value = '';
        phoneInputSale.value = '';
        phoneErrorSale.innerText = '';
        nameErrorSale.innerText = '';
        nameErrorSale.classList.remove('success');
        phoneErrorSale.classList.remove('error');
        phoneErrorSale.classList.remove('success');
        nameErrorSale.classList.remove('error');
        phoneInputSale.classList.remove('success');
        nameInputSale.classList.remove('success');
        phoneInputSale.classList.remove('error');
        nameInputSale.classList.remove('error');

        formBtn.forEach((e) => {
          e.blur();
        })
      }, 3000);

    }
  });
}




const searchInputNameSale = document.querySelectorAll(".white-inp-name-Sale");
function clearNameSale() {
  nameInputSale.value = '';
  nameInputSale.classList.remove('error');
  nameInputSale.classList.remove('success');
  nameErrorSale.classList.remove('error');
  nameErrorSale.classList.remove('success');
  nameErrorSale.innerText = '';

}
const searchInputPhoneSale = document.querySelectorAll(".white-inp-phone-Sale");
function clearPhoneSale() {
  phoneInputSale.value = '';
  phoneInputSale.classList.remove('error');
  phoneInputSale.classList.remove('success');
  phoneErrorSale.classList.remove('error');
  phoneErrorSale.classList.remove('success');
  phoneErrorSale.innerText = '';
}
// код главной формы с текстом "Скидка"

// -----------------------// -----------------------// -----------------------// -----------------------

// код для поисковика

const searchInput = document.querySelector(".check-input");
function clearSearch() {
  searchInput.value = '';
}

// код для поисковика

// -----------------------// -----------------------// -----------------------// -----------------------

// input close / checker

// window.addEventListener("DOMContentLoaded", function () {
//   [].forEach.call(
//     document.querySelectorAll(".white-inp-phone"),
//     function (input) {
//       var keyCode;
//       function mask(event) {
//         event.keyCode && (keyCode = event.keyCode);
//         var pos = this.selectionStart;
//         if (pos < 3) event.preventDefault();
//         var matrix = "+7 (___) ___ ____",
//           i = 0,
//           def = matrix.replace(/\D/g, ""),
//           val = this.value.replace(/\D/g, ""),
//           new_value = matrix.replace(/[_\d]/g, function (a) {
//             return i < val.length ? val.charAt(i++) || def.charAt(i) : a;
//           });
//         i = new_value.indexOf("_");
//         if (i != -1) {
//           i < 5 && (i = 3);
//           new_value = new_value.slice(0, i);
//         }
//         var reg = matrix
//           .substr(0, this.value.length)
//           .replace(/_+/g, function (a) {
//             return "\\d{1," + a.length + "}";
//           })
//           .replace(/[+()]/g, "\\$&");
//         reg = new RegExp("^" + reg + "$");
//         if (
//           !reg.test(this.value) ||
//           this.value.length < 5 ||
//           (keyCode > 47 && keyCode < 58)
//         )
//           this.value = new_value;
//         if (event.type == "blur" && this.value.length < 5) this.value = "";
//         // console.log(input.value.length);
//         // formBtn.forEach((e) => {
//         //   // if (input.value.length == "17") {
//         //   //   e.removeAttribute("disabled");
//         //   // } else {
//         //   //   e.setAttribute("disabled", true);
//         //   // }


//         // });
//       }

//       input.addEventListener("input", mask, false);
//       input.addEventListener("focus", mask, false);
//       input.addEventListener("blur", mask, false);
//       input.addEventListener("keydown", mask, false);
//     }
//   );
// });





// document.addEventListener("click", (e) => {
//   // Вешаем обработчик на весь документ
//   if (e.target == popupBgCity) {
//     // Если цель клика - фон, то:
//     popupBgCity.classList.remove("active"); // Убираем активный класс с фона
//     popup.classList.remove("active"); // И с окна
//     const body = document.body;
//     body.style.height = "";
//     body.style.overflowY = "";
//   } else if (e.target == popupBgForm) {
//     popupBgForm.classList.remove("active"); // Убираем активный класс с фона
//     popupAddress.classList.remove("active"); // И с окна
//     const body = document.body;
//     body.style.height = "";
//     body.style.overflowY = "";
//   } else if (e.target == popupNum) {
//     popupBgForm.classList.remove("active"); // Убираем активный класс с фона
//     popupAddress.classList.remove("active"); // И с окна
//     popupNum.classList.remove("active");
//     const body = document.body;
//     body.style.height = "";
//     body.style.overflowY = "";
//     popupBgCity.classList.remove("active"); // Убираем активный класс с фона
//     popup.classList.remove("active"); // И с окна
//     popupNumBox.classList.remove("active");
//   }
// });

// modals
if (window.innerWidth < 830) {
  $(document).ready(function () {
    // 250 characters are shown by default
    var showChar = 100;
    var dots = "..."
    var moreText = "читать дальше";
    var lessText = "Скрыть";

    $('.item-text').each(function () {
      var content = $(this).html();

      if (content.length > showChar) {
        console.log(content.length)
        var cont = content.substr(0, showChar);
        var restOfTheText = content.substr(showChar, content.length - showChar);

        var html = cont + '<span class="dots">' + dots + '</span><span class="morecontent"><span>' + restOfTheText + '</span><a href="" class="morelink">' + moreText + '</a></span>';

        $(this).html(html);
      }

    });
    $(".morelink").click(function () {
      if ($(this).hasClass("test")) {
        $(this).removeClass("test");
        $(this).html(moreText);
      } else {
        $(this).addClass("test");
        $(this).html(lessText);
      }
      $(this).parent().prev().toggle();
      $(this).prev().toggle();
      return false;
    });
  });
}

let templeBtn = document.querySelectorAll('.letter-place')
let title = document.querySelector('.temple-tilte')
templeBtn.forEach((button) => {
  // Перебираем все кнопки
  button.addEventListener("click", (e) => {
    console.log(button.classList.value)
    // Для каждой вешаем обработчик событий на клик
    e.preventDefault(); // Предотвращаем дефолтное поведение браузера
    if (button.classList.value == "letter-place") {
      title.innerText = button.innerText
    }
    // if (button.classList[0] == "city-changer") {
    //   popupBgCity.classList.add("active"); // Добавляем класс 'active' для фона
    //   popupAddress.classList.add("active"); // И для самого окна
    //   menu.forEach((e) => {
    //     e.classList.remove("active");
    //   });
    //   const body = document.body;
    //   body.style.overflowY = "hidden";
    // } else {
    //   popupBgForm.classList.add("active"); // Добавляем класс 'active' для фона
    //   popup.classList.add("active"); // И для самого окна
    //   console.log(Title)
    //    else if (button.classList[0] == "type__switcher-colorBtn") {
    //     Title.innerText = 'Не нашли свою поломку?'
    //   } else {
    //     Title.innerText = 'Обратный звонок'
    //   }
    //   const body = document.body;
    //   body.style.overflowY = "hidden";
    // }
  });

});

document.addEventListener("DOMContentLoaded", () => {
  const inputBox = document.querySelector(".input-box");
  const phrases = Array.from(document.querySelectorAll(".findRepair-item")).map(el => el.textContent);

  if (!inputBox || phrases.length === 0) return;

  let index = 0;
  let charIndex = 0;
  let isDeleting = false;

  function typeEffect() {
    const currentPhrase = phrases[index];

    if (!isDeleting) {
      inputBox.textContent = currentPhrase.slice(0, charIndex++);
      if (charIndex > currentPhrase.length) {
        isDeleting = true;
        setTimeout(typeEffect, 1000);
        return;
      }
    } else {
      inputBox.textContent = currentPhrase.slice(0, charIndex--);
      if (charIndex === 0) {
        isDeleting = false;
        index = (index + 1) % phrases.length;
      }
    }

    setTimeout(typeEffect, isDeleting ? 50 : 100);
  }

  typeEffect();
});

$(document).ready(function () {

  $(window).scroll(function() {

    var topPos = $(this).scrollTop();
    
    if (topPos > 100) {
      $('.phone_block').addClass('visible');

    } else {
      $('.phone_block').removeClass('visible');
    }

  });
  // menu-brands

  $(".brands-btn-open").on("click", function () {
    $(".brands-list").toggleClass("open");
  });

  $(".repair_box-open").on("click", function(){
    $(this).parent().toggleClass("open").hasClass("open") 
        ? $(this).text("Скрыть") 
        : $(this).text("Показать больше поломок");
  })

  // menu-brands
  // toggler catalog
  $(".btn-open").on("click", function () {
    $(this).parent().parent().toggleClass("open");
  });
  $(".content-list-open").on("click", function () {
    $(this).parent().toggleClass("open");
    $(this).text() = ($(this).text() == 'Показать весь список') ? 'Скрыть' : 'Показать весь список';
  });
  // toggler price
  // $(".new-rev .item-bottom .button_center").on("click", function () {
  //   $(".item-bottom").toggleClass("open");
  // });
  // Правки 03.09.2026 (правки заказчика, п. «Прайс»): при раскрытом прайсе
  // на кнопке должно быть «Скрыть». Было: подпись не менялась — раскрытый
  // прайс предлагал «Показать полностью» второй раз.
  // Подписи берём из data-атрибутов кнопки (php_blocks/price-block.php),
  // если их нет — работает прежнее поведение без смены текста.
  $(".other-btn-price").on("click", function () {
    var open = $(".price-table").toggleClass("open").hasClass("open");
    var more = $(this).attr("data-more");
    var less = $(this).attr("data-less");
    if (more && less) {
      $(".other-btn-price").text(open ? less : more);
    }
  });
  $(".item-table-btn").on("click", function () {
    $(".tablewrap").toggleClass("open");
  });
  $(".other-btn").on("click", function () {
    $(".other-cards").toggleClass("open");
  });
  $(window).scroll(function () {
    var scroll = $(window).scrollTop();

    if (scroll >= 0) {
      $("#head").addClass("scrolled");
    } else {
      $("#head").addClass("scrolled");
    }
  });
  //Tabs
  function tabs($class) {
    $(".tab-item").on("click", function () {
      let $current_tab = $(this).closest($class);
      let $tab_id = $(this).attr("data-tab");

      $($current_tab).find(".tab-item").removeClass("btn_style_outfilled");
      $($current_tab)
        .find(".tab-content__item")
        .removeClass("tab-content__item_active");
      $($tab_id).addClass("tab-content__item_active");
      $(this).addClass("btn_style_outfilled");
    });
  }

  tabs(".cost-block");



  var customOptions = {
    onKeyPress: function (val, e, field, options) {
      if (val.replace(/\D/g, "").length === 2) {
        val = val.replace("8", "");
        field.val(val);
      }
      field.mask("+7 (000) 000-00-00", options);
    },
    // placeholder: "+7 (000) 000-00-00",
  };
  $('[inputmode="tel"]').mask("+7 (000) 000-00-00", customOptions);
  $('form button').attr('disabled', false);



  $("form").on("submit", function (event) {

    event.preventDefault();

    let urlForm = $("#url-ajax-form").val(); // sendform
    let title = $(this).find('input[name="title"]').val();
    let name = $(this).find('input[name="your-name"]').val();
    let phone = $(this).find('input[name="your-tel"]').val();
    let select = $(this).find('input[name="select"]').val();
    // let breakdown = $(this).find('[name="your-breakdown"]').val();
    let textarea = $(this).find('[name="your-textarea"]').val();
    let metrika = $("#metrika-ajax-form").val();
    let domain = $("#domain-ajax-form").val();

    // Правки 20.08.2026: промо-код из блока «Акции и скидки».
    // Заголовок акции подменяет тему заявки, чтобы в CRM было видно источник.
    let promo = $(this).find('input[name="promo"]').val();
    let promoTitle = $(this).find('input[name="promo_title"]').val();
    if (promo && promoTitle) {
      title = promoTitle;
    }

    let data = {
      title: title,
      name: name,
      phone: phone,
      message: textarea,
      select: select,
      promo: promo,
    };

    let phoneTrue = phone;
    phoneTrue = phoneTrue.match(/\d+/g);
    phoneTrue = phoneTrue ? phoneTrue.join('') : '';
    // console.log('значения:' + phoneTrue + ' кол-во сим:' + phoneTrue.length);

    if (phoneTrue.length == 11) {

      $.ajax({
        url: urlForm,
        type: "POST",
        data: data,
        success: function (response) {

          // console.log(response);
          if (response == 1) {
            if (metrika) {
              ym(metrika, "reachGoal", domain);
            }
            // -----------------------------------------------------------------
            setTimeout(function () {
              $(".overlay").removeClass("overlay_active");
              $(".modal_size_small").removeClass("modal_active");
            }, 1500);
            alert('Номер отправлен');
            // -----------------------------------------------------------------
            $('[inputmode="tel"]').val("");
            // Промо-код одноразовый — чистим, чтобы он не уехал со следующей заявкой
            $('input[name="promo"], input[name="promo_title"]').val("");
            $("body").css({ "overflow": "inherit" });
            $("body").css({ "height": "inherit" });
          } else {
            alert('Сообщение не доставлено, попробуйте еще раз');
            $('[inputmode="tel"]').val("");
          }

        },
      });

    } else {
      alert('Некорректный номер');
      $('[inputmode="tel"]').val("");
    }

  });

  $(".tabel-check__reload").on("click", function () {
    $(".tabel-check").removeClass("tabel-check_active");
    $(".check-form__number").val("");
  });

  //Show more services
  $(".services-section__btn").on("click", function () {
    var $current_block = $(this)
      .closest(".services-section")
      .find(".services-block");
    var $text_before = $(this).attr("data-textbefore");
    var $text_after = $(this).attr("data-textafter");

    if ($current_block.hasClass("services-block_collapsed") === true) {
      $current_block.removeClass("services-block_collapsed");
      $(this).text($text_after);
    } else {
      $current_block.addClass("services-block_collapsed");
      $(this).text($text_before);
    }
  });

  //Form Validation
  // $('form[data-leadform=""]').on("ready keyup", function () {
  //   let form = $(this).find('[inputmode="tel"]').val().length;
  //   if (form == 18) {
  //     $(this).find(".form__submit").attr("disabled", null);
  //   } else {
  //     $(this).find(".form__submit").attr("disabled", "disabled");
  //   }
  // });

  //Modals
  $(document).mouseup(function (e) {
    var $modal = $(".modal");
    var $overlay = $(".overlay");
    if (!$modal.is(e.target) && $modal.has(e.target).length === 0) {
      $modal.removeClass("modal_active");
      $overlay.removeClass("overlay_active");
      $("body").css({ "overflow": "visible" })
    }
  });

  $(".modal__close").on("click", function () {
    $(".overlay").removeClass("overlay_active");
    $(".modal").removeClass("modal_active");
    $("body").css({ "overflow": "visible" })
  });

  $('.show-cat-card button').click(function () {
    $('.catalog .catalog-cards').toggleClass('no_show_card');
    if ($(this).text() == 'Показать больше') {
      $(this).text('Скрыть');
    } else {
      $(this).text('Показать больше');
    }
  });

});






$(document).ready(function () {

  $(window).scroll(function () {
    var $element = $('.cat-button.has-parent'); // указать класс вашего элемента
    var distanceTop = $element.offset().top;
    var scrollTop = $(window).scrollTop();
    var distanceToTop = distanceTop - scrollTop;
    let upMenu = distanceToTop - 26;
    $('.devices-menu').css('top', upMenu);
  });


  // Главное окно бургер
  $('.cat-button.has-parent').click(function () {
    $('.devices-box').toggleClass('active');
    $('body, html').toggleClass('stop_scroll');
    $(this).toggleClass('active_menu');
  });

  $('.bg_devices-box').click(function () {
    $('.devices-box').removeClass('active');
    $('body, html').removeClass('stop_scroll')
    $('.cat-button.has-parent').removeClass('active_menu');
  });

  $('.catalog-uslug').click(function () {
    $('.mob-menu-catalog').slideToggle();
  });

  $('.click__drop_menu').click(function () {
    $(this).next().slideToggle();
  });

  var visibleMenu;

  $(".link_2lv").hover(function () {
    var $this = $(this);
    if (visibleMenu) {
      visibleMenu.hide();
      $(".link_2lv").removeClass("up-text");
    }

    $(".multimenu-3lv").hide();
    var $menu3lv = $this.next(".multimenu-3lv");

    $this.addClass("up-text"); // Добавляем класс при открытии меню

    var menuPosition = $menu3lv.offset();
    var menuWidth = $menu3lv.outerWidth();
    var menuHeight = $menu3lv.outerHeight();
    var deviceMenuPosition = $(".devices-menu").offset();
    var deviceMenuWidth = $(".devices-menu").outerWidth();
    var deviceMenuHeight = $(".devices-menu").outerHeight();

    if (menuPosition.left + menuWidth > deviceMenuPosition.left + deviceMenuWidth) {
      menuPosition.left = deviceMenuPosition.left + deviceMenuWidth - menuWidth;
    }

    if (menuPosition.top + menuHeight > deviceMenuPosition.top + deviceMenuHeight) {
      if (menuPosition.top < deviceMenuPosition.top) {
        menuPosition.top = deviceMenuPosition.top;
      } else {
        menuPosition.top = deviceMenuPosition.top + deviceMenuHeight - menuHeight;
      }
    }

    $menu3lv.css(menuPosition);
    $menu3lv.show();
    visibleMenu = $menu3lv;
  });


  $(".devices-menu").mouseleave(function () {
    if (visibleMenu) {
      visibleMenu.hide();
      $(".link_2lv").removeClass("up-text"); // Удаляем класс при скрытии меню
    }
  });


  // if ($(window).width() < 992) {
  //   function relocateStar() {
  //     $('.main-window').each(function () {
  //       const star = $(this).find('.line-utp span.star').first(); // Берем первый элемент `.star`
  //       const obolo4ka = $(this).find('.obolo4ka');
  //       const lineUtp = $(this).find('.line-utp');

  //       // Удаляем лишние копии `.star`, если они существуют
  //       $(this).find('.line-utp span.star').not(star).remove();
  //       $(this).find('.obolo4ka span.star').not(star).remove();

  //       if ($(window).width() < 992) {
  //         if (!star.parent().is(lineUtp)) {
  //           lineUtp.prepend(star); // Перемещаем в `.line-utp`, если `.star` не там
  //         }
  //       } else {
  //         if (!star.parent().is(obolo4ka)) {
  //           obolo4ka.prepend(star); // Перемещаем в `.obolo4ka`, если `.star` не там
  //         }
  //       }
  //     });
  //   }

  //   // Вызываем функцию при загрузке страницы
  //   relocateStar();

  //   // Вызываем функцию при изменении размера окна
  //   $(window).resize(relocateStar);
  // } else {
  //   function relocateStar() {
  //     $('.main-window').each(function () {
  //       const lineUtp = $(this).find('.line-utp');
  //       const items = lineUtp.children('.item'); // Каждый пункт, над которым должна быть звезда

  //       if ($(window).width() < 992) {
  //         // Мобильная версия: перемещаем одну звезду в начало `.line-utp`
  //         const star = $(this).find('span.star').first(); // Находим первую звезду
  //         lineUtp.prepend(star); // Перемещаем ее в начало `.line-utp`

  //         // Удаляем лишние звезды, если остались
  //         $(this).find('span.star').not(star).remove();
  //       } else {
  //         // ПК-версия: добавляем звезду над каждым пунктом, если её там нет
  //         items.each(function () {
  //           if (!$(this).children('span.star').length) {
  //             // Добавляем звезду, если её ещё нет
  //             $(this).prepend('<span class="star">⭐</span>');
  //           }
  //         });
  //       }
  //     });
  //   }

  //   // Вызываем функцию при загрузке страницы
  //   relocateStar();

  //   // Вызываем функцию при изменении размера окна
  //   $(window).resize(relocateStar);
  // }




  $(".new-rev .button_center").on("click", function () {

    var count = $('.single-rev').length;
    count = count + 4;

    let mark = $(this).data('brand');
    let device = $(this).data('device');
    let model = $(this).data('model');
    let route = $(this).data('route');

    let data = {
      count: count,
      route: route,
      model: model,
      device: device,
      mark: mark
    }

    // console.log(data);
    $.ajax({
      type: "post",
      url: $('#url-review').val(),
      data: data,
      success: function (html) {
        $('.item-bottom').html(html)
      }
    });

  });



});