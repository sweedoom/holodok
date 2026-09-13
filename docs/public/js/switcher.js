// seo-box

let headerSeo = document.querySelector('.inner-tabs')

if(headerSeo !== null) {
    window.addEventListener('DOMContentLoaded', function() {

        'use strict';
        let tab = document.querySelectorAll('.inner-tabs-item'),
            headerSeo = document.querySelector('.inner-tabs'),
            tabContent = document.querySelectorAll('.inner-tabs-content');
        
      
            
        function hideTabContent(a) {
            for (let i = a; i < tabContent.length; i++) {
                tabContent[i].classList.remove('show');
                tabContent[i].classList.add('hide');
            }
        }
      
        hideTabContent(1);
      
        function showTabContent(b) {
          
            if (tabContent[b].classList.contains('hide')) {
                tabContent[b].classList.remove('hide');
                tabContent[b].classList.add('show');
            }
        }
      
        headerSeo.addEventListener('click', function(event) {
          
            let target = event.target;
            if (target && target.classList.contains('inner-tabs-item')) {
              
                for(let i = 0; i < tab.length; i++) {
                    if (target == tab[i]) {
                      
                        hideTabContent(0);
                        showTabContent(i);
                        break;
                    }
                }
            }
      
        });
      });
      
      const activeBtn4 = document.querySelectorAll(".inner-tabs-item");
      
      activeBtn4.forEach((btn) => {
        btn.addEventListener("click", (e) => {
          activeBtn4.forEach((f) => f.classList.remove("active"));
          e.target.classList.toggle("active");
        });
      });
}



// seo-box


// how-switcher

window.addEventListener('DOMContentLoaded', function() {

  'use strict';
  let tab = document.querySelectorAll('.how-switch-btn'),
      header = document.querySelector('.how_inner-cards'),
      tabContent = document.querySelectorAll('.how_switcher-item');
  

      
  function hideTabContent(a) {
      for (let i = a; i < tabContent.length; i++) {
          tabContent[i].classList.remove('show');
          tabContent[i].classList.add('hide');
      }
  }

  hideTabContent(1);

  function showTabContent(b) {
    
      if (tabContent[b].classList.contains('hide')) {
          tabContent[b].classList.remove('hide');
          tabContent[b].classList.add('show');
      }
  }

  header.addEventListener('click', function(event) {
    
      let target = event.target;
      if (target && target.classList.contains('how-switch-btn')) {
        
          for(let i = 0; i < tab.length; i++) {
              if (target == tab[i]) {
                
                  hideTabContent(0);
                  showTabContent(i);
                  break;
              }
          }
      }

  });
});

const activeBtn = document.querySelectorAll(".how-switch-btn");

activeBtn.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    activeBtn.forEach((f) => f.classList.remove("active"));
    e.target.classList.toggle("active");
  });
});

// how-switcher


// faq-switcher


window.addEventListener('DOMContentLoaded', function() {

    'use strict';
    let tab = document.querySelectorAll('.faq_cards-item'),
        header = document.querySelector('.faq_cards'),
        tabContent = document.querySelectorAll('.faq-text');
    
  
        
    function hideTabContent(a) {
        for (let i = a; i < tabContent.length; i++) {
            tabContent[i].classList.remove('show');
            tabContent[i].classList.add('hide');
        }
    }
  
    hideTabContent(1);
  
    function showTabContent(b) {
      
        if (tabContent[b].classList.contains('hide')) {
            tabContent[b].classList.remove('hide');
            tabContent[b].classList.add('show');
        }
    }
  
    header.addEventListener('click', function(event) {
      
        let target = event.target;
        if (target && target.classList.contains('faq_cards-item')) {
          
            for(let i = 0; i < tab.length; i++) {
                if (target == tab[i]) {
                  
                    hideTabContent(0);
                    showTabContent(i);
                    break;
                }
            }
        }
  
    });
  });


const activeBtn1 = document.querySelectorAll(".faq_cards-item");

activeBtn1.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    activeBtn1.forEach((f) => f.classList.remove("active"));
    e.target.classList.toggle("active");
  });
});

// faq-switcher


// models-switcher

window.addEventListener('DOMContentLoaded', function() {

    'use strict';
    let tab = document.querySelectorAll('.models-switcher-btn'),
        header = document.querySelector('.models-switcher'),
        tabContent = document.querySelectorAll('.catalog-cards');
    
  
        
    function hideTabContent(a) {
        for (let i = a; i < tabContent.length; i++) {
            tabContent[i].classList.remove('show');
            tabContent[i].classList.add('hide');
        }
    }
  
    hideTabContent(1);
  
    function showTabContent(b) {
      
        if (tabContent[b].classList.contains('hide')) {
            tabContent[b].classList.remove('hide');
            tabContent[b].classList.add('show');
        }
    }
    if(header === null){

    } else{
        header.addEventListener('click', function(event) {
      
            let target = event.target;
            if (target && target.classList.contains('models-switcher-btn')) {
              
                for(let i = 0; i < tab.length; i++) {
                    if (target == tab[i]) {
                      
                        hideTabContent(0);
                        showTabContent(i);
                        break;
                    }
                }
            }
      
        });
    }
    
  });


const activeBtn2 = document.querySelectorAll(".models-switcher-btn");

activeBtn2.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    activeBtn2.forEach((f) => f.classList.remove("active"));
    e.target.classList.toggle("active");
  });
});

// models-switcher

// device page switcher how

window.addEventListener('DOMContentLoaded', function() {

    'use strict';
    let tab = document.querySelectorAll('.how_inner-switch'),
        header = document.querySelector('.vol-2'),
        tabContent = document.querySelectorAll('.how_inner-switch');
    
  
        
    function hideTabContent(a) {
        for (let i = a; i < tabContent.length; i++) {
            tabContent[i].classList.remove('show');
            tabContent[i].classList.add('hide');
        }
    }
  
    hideTabContent(1);
  
    function showTabContent(b) {
      
        if (tabContent[b].classList.contains('hide')) {
            tabContent[b].classList.remove('hide');
            tabContent[b].classList.add('show');
        }
    }
  
    header.addEventListener('click', function(event) {
      
        let target = event.target;
        if (target && target.classList.contains('how_inner-switch')) {
          
            for(let i = 0; i < tab.length; i++) {
                if (target == tab[i]) {
                  
                    hideTabContent(0);
                    showTabContent(i);
                    break;
                }
            }
        }
  
    });
  });


const activeBtn3 = document.querySelectorAll(".how_inner-switch");

activeBtn3.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    activeBtn3.forEach((f) => f.classList.remove("active"));
    e.target.classList.toggle("active");
  });
});

// device page switcher how


