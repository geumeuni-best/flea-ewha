function initRatingText() {
  var ratingGroup = document.querySelector('fieldset.rating');
  var ratingText = document.getElementById('rating-text');

  if (!ratingGroup || !ratingText) return;

  function getCurrentValue() {
    var checked = ratingGroup.querySelector('input[name="rating"]:checked');
    if (!checked) return '0';
    return checked.value;
  }

  function render() {
    var value = getCurrentValue();
    ratingText.textContent = value + '/5';
  }

  render();

  var radios = ratingGroup.querySelectorAll('input[name="rating"]');
  radios.forEach(function (r) {
    r.addEventListener('change', render);
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initRatingText();
});

window.updateFileName = window.updateFileName || function (input) {
  var fileNameSpan = document.getElementById('file-name');
  if (!fileNameSpan) return;
  if (!input || !input.files || !input.files.length) {
    fileNameSpan.textContent = '';
    return;
  }
  fileNameSpan.textContent = input.files[0].name;
};
