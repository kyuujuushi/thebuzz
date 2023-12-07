const link = encodeURI(winndow.location.href);
const mes = encodeURIComponent('Look at These Events!');
const title = encodeURIComponent('Article or Post Title Here');

const reddit = document.querySelector('.reddit');
reddit.href = `http://www.reddit.com/submit?url=${link}&title=${title}`;
const Twitter

const linkedin

const fb = document.querySelector('.facebook');
fb.href = `https://www.facebook.com/share.php?u=${link}`;