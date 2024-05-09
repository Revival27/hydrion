function toggleText() {
    var moreText = document.getElementById('more_text');
    var moreButton = document.querySelector('#btn-description');
    if (moreText.style.display === 'none') {
        moreText.style.display = 'inline';
        moreButton.textContent = 'Less';
    } else {
        moreText.style.display = 'none';
        moreButton.textContent = 'More';
    }
}