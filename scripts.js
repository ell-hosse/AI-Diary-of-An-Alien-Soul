let currentIndex = 0;

function openModalByIndex(index) {
  currentIndex = index;
  const item = window.galleryData[index];

  const modal = document.getElementById('modal');
  const img = document.getElementById('modal-img');
  const caption = document.getElementById('modal-caption');

  img.src = 'images/thumbs/' + item.filename;
  img.style.filter = 'blur(10px)';
  caption.textContent = `${item.title} — ${item.creation_date.split(' ')[0]}`;

  modal.style.display = 'flex';
  document.body.classList.add('modal-open');

  const full = new Image();
  full.src = 'images/original/' + item.filename;
  full.onload = () => {
    img.src = full.src;
    img.style.filter = 'none';
  };
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
  document.body.classList.remove('modal-open');
}

function prevImage() {
  if (currentIndex > 0) {
    openModalByIndex(currentIndex - 1);
  }
}

function nextImage() {
  if (currentIndex < window.galleryData.length - 1) {
    openModalByIndex(currentIndex + 1);
  }
}

// Close modal on ESC
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
  if (e.key === 'ArrowLeft') prevImage();
  if (e.key === 'ArrowRight') nextImage();
});
