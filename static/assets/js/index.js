
document.addEventListener('click', (e) => {
    if (e.target.closest('.remove-btn')) {
        const btn = e.target.closest('.remove-btn');
        const productId = btn.dataset.productId;

        fetch(`/toggle-wishlist/${productId}/`)
            .then(response => response.json())
            .then(data => {
                if (!data.liked) {
                    // Remove product card from DOM
                    const card = document.querySelector(`.wishlist-card[data-product-id="${productId}"]`);
                    if (card) card.remove();
                }
            });
    }
});