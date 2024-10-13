document.addEventListener('DOMContentLoaded', function () {
  // Read more
  const readMoreBtns = document.querySelectorAll('.read-more-btn');
  const textElements = document.querySelectorAll('.tutors-list-item-bio');
  const previewLength = 50;
  let fullTexts = [];

  textElements.forEach((element, index) => {
    fullTexts[index] = element.getAttribute('data-full-text');
    if (fullTexts[index].length > previewLength) {
      const previewText = fullTexts[index].substring(0, previewLength) + '...';
      element.textContent = previewText;

      readMoreBtns[index].addEventListener('click', function () {
        if (element.textContent === previewText) {
          element.textContent = fullTexts[index];
          this.textContent = 'Read Less';
        } else {
          element.textContent = previewText;
          this.textContent = 'Read More';
        }
      });
    } else {
      readMoreBtns[index].style.display = 'none';
    }
  });
});
