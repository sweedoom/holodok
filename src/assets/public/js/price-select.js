// document.addEventListener('DOMContentLoaded', function () {
//     const customSelect = document.querySelector('.custom-select');
//     const selectSelected = customSelect.querySelector('.select-selected');
//     const selectItems = customSelect.querySelector('.select-items');
//     const selectOptions = customSelect.querySelectorAll('.select-items li');
  
//     // При клике на кастомный select открываем/закрываем выпадающий список
//     selectSelected.addEventListener('click', function () {
//       selectItems.style.display = selectItems.style.display === 'block' ? 'none' : 'block';
//     });
  
//     // При выборе опции из выпадающего списка
//     selectOptions.forEach(function (option) {
//       option.addEventListener('click', function () {
//         selectSelected.textContent = option.textContent;
//         selectItems.style.display = 'none';
//       });
//     });
  
//     // Закрыть выпадающий список при клике вне него
//     window.addEventListener('click', function (e) {
//       if (!customSelect.contains(e.target)) {
//         selectItems.style.display = 'none';
//       }
//     });
//   });
  
  

// price-switcher
// Получаем элементы select и все таблицы с классом "hidden"
const select = document.getElementById("custom-options-id");
const tables = document.querySelectorAll(".price-table");

// Обработчик изменения значения select
function showSelectedTable() {
    // Скрываем все таблицы
    tables.forEach(table => {
      table.classList.add('hide');
    });
  
    // Отображаем выбранную таблицу
    const selectedTableId = select.value;
    const selectedTable = document.getElementById(selectedTableId);
    if (selectedTable) {
      selectedTable.classList.remove('hide');
    }
  }
  
  // Вызываем обработчик при загрузке страницы для отображения первой таблицы
  showSelectedTable();
  
  // Добавляем обработчик изменения select
  select.addEventListener('change', showSelectedTable);
// price-switcher

