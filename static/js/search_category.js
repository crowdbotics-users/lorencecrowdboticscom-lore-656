$(document).ready(function() {
  $('.search-category').selectpicker();

  $('.search-category').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    e.preventDefault();

    var category = $(this).val();
    var url = `${window.location.pathname}?category=${category}`;

    if (category) {
      window.location = url;
    }
  });
});
