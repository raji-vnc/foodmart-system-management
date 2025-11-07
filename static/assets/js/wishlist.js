
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.remove-btn');
  if (btn) {
    e.preventDefault(); // prevent refresh
    const productId = btn.dataset.productId;

    fetch(`/toggle-wishlist/${productId}/`)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'removed') {
          // remove card from page instantly
          btn.closest('.wishlist-card').remove();
        }
      })
      .catch(error => console.error('Error:', error));
  }
});
