var swiper = new Swiper(".mySwiper", {
  centeredSlides: true,
  slidesPerView: 1,
  initialSlide: 2,
  spaceBetween: -60,
  loop: true,
  grabCursor: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    650: {
      slidesPerView: 1,
      initialSlide: 2,
      spaceBetween: -260,
    },
    830: {
      slidesPerView: 1,
      spaceBetween: -485,
      autoHeight: true,
      initialSlide: 2,
    },
    1050: {
      slidesPerView: 2,
      initialSlide: 2,
      spaceBetween: -164,
    },
  },
});
var swiper = new Swiper(".mySwiperEx", {
  slidesPerView: 1,
  // centeredSlidesBounds:true,
  spaceBetween: 32,
  autoHeight: true,

  loop: true,
  grabCursor: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    1050: {
      centeredSlides: true,
      slidesPerView: 3,
      spaceBetween: 25,
    },
  },
});
var swiper = new Swiper(".mySwiper1", {
  slidesPerView: 1,
  spaceBetween: 32,
  autoHeight: true,
  // loop: true,
  grabCursor: true,
  breakpoints: {
    1050: {
      // centeredSlides: true,
      slidesPerView: 3,
      // initialSlide: 1,
      spaceBetween: 25,
    },
  },
});
