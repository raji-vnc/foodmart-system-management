document.addEventListener('DOMContentLoaded', function () {
  document.body.addEventListener('click', function (e) {
    if (e.target.classList.contains('loveicon')) {
      const icon = e.target;
      const productId = icon.dataset.productId;

      fetch(`/toggle-wishlist/${productId}/`)
        .then(response => response.json())
        .then(data => {
          if (data.liked) {
            icon.classList.add('active');
          } else {
            icon.classList.remove('active');
          }
        })
        .catch(err => console.error('Wishlist toggle error:', err));
    }
  });
});

