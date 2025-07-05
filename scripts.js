let currentIndex = 0;

function openModalByIndex(index) {
  console.log("Clicked image:", index);
  const data = window.galleryData;
  currentIndex = index;
  const item = data[index];

  const modal = document.getElementById('modal');
  const modalImg = document.getElementById('modal-img');
  const caption = document.getElementById('modal-caption');

  // Blur-up effect
  modalImg.src = 'images/thumbs/' + item.filename;
  modalImg.style.filter = 'blur(10px)';
  modal.style.display = 'block';
  caption.innerText = `${item.title} — ${item.creation_date.split(" ")[0]}`;

  const fullResImg = new Image();
  fullResImg.src = 'images/original/' + item.filename;
  fullResImg.onload = () => {
    modalImg.src = fullResImg.src;
    modalImg.style.filter = 'none';
  };
}

function closeModal() {
  document.getElementById('modal').style.display = "none";
}

function prevImage() {
  if (currentIndex > 0) openModalByIndex(--currentIndex);
}

function nextImage() {
  if (currentIndex < window.galleryData.length - 1) openModalByIndex(++currentIndex);
}