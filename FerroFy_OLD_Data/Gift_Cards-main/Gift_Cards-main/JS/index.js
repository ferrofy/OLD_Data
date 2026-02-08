document.addEventListener("DOMContentLoaded", () => {
    const MAX_ALL = 10000000;
    const giftCards = [
        { name: 'Amazon', discount: '1%', min: 10, max: MAX_ALL, image: './IMG/Amazon.png', tags: ['E-Commerce'] },
        { name: 'Play Store', discount: '2%', min: 10, max: MAX_ALL, image: './IMG/Play_Store.png', tags: ['Gaming'] },
        { name: 'AJIO', discount: '3%', min: 10, max: MAX_ALL, image: './IMG/AJIO.png', tags: ['Fashion'] },
        { name: 'Myntra', discount: '2%', min: 250, max: MAX_ALL, image: './IMG/Myntra.png', tags: ['Fashion'] },
        { name: 'Zepto', discount: '2%', min: 100, max: MAX_ALL, image: './IMG/Zepto.png', tags: ['Food'] },
        { name: 'KFC', discount: '3%', min: 100, max: MAX_ALL, image: './IMG/KFC.png', tags: ['Food'] },
        { name: 'Book My Show', discount: '3%', min: 100, max: MAX_ALL, image: './IMG/Book_My_Show.png', tags: ['Trip'] },
        { name: 'PVR', discount: '7%', min: 100, max: MAX_ALL, image: './IMG/PVR.png', tags: ['Movie'] },
        { name: 'Barbeque Nation', discount: '4%', min: 500, max: MAX_ALL, image: './IMG/Barbeque_Nation.png', tags: ['Food'] },
        { name: 'Fab India', discount: '5%', min: 250, max: MAX_ALL, image: './IMG/Fab_India.png', tags: ['Fashion'] },
        { name: 'Fastrack', discount: '5%', min: 500, max: MAX_ALL, image: './IMG/Fastrack.png', tags: ['Other'] },
        { name: 'Big Basket', discount: '1.5%', min: 50, max: MAX_ALL, image: './IMG/Big_Basket.png', tags: ['Food'] },
        { name: 'Croma', discount: '2%', min: 500, max: MAX_ALL, image: './IMG/Croma.png', tags: ['E-Commerce'] },
        { name: 'Lakme', discount: '2%', min: 500, max: MAX_ALL, image: './IMG/Lakme.png', tags: ['Fashion'] },
        { name: 'V Mart', discount: '3%', min: 100, max: MAX_ALL, image: './IMG/V_Mart.png', tags: ['E-Commerce'] },
        { name: 'Nykaa', discount: '5%', min: 10, max: MAX_ALL, image: './IMG/Nykaa.png', tags: ['Fashion'] },
        { name: 'MamaEarth', discount: '7%', min: 500, max: MAX_ALL, image: './IMG/MamaEarth.png', tags: ['Fashion'] },
        { name: 'Dominos', discount: '7%', min: 100, max: MAX_ALL, image: './IMG/Dominos.png', tags: ['Food'] },
        { name: 'Puma', discount: '6%', min: 500, max: MAX_ALL, image: './IMG/Puma.png', tags: ['Fashion'] },
        { name: 'My Glamm', discount: '8%', min: 250, max: MAX_ALL, image: './IMG/My_Glamm.png', tags: ['Fashion'] },
        { name: 'Himalaya', discount: '1%', min: 100, max: MAX_ALL, image: './IMG/Himalaya.png', tags: ['Fashion'] },
        { name: 'Bewakoof', discount: '6%', min: 500, max: MAX_ALL, image: './IMG/Bewakoof.png', tags: ['Fashion'] },
        { name: 'Cafe Coffee Day', discount: '6%', min: 100, max: MAX_ALL, image: './IMG/Cafe_Coffee_Day.png', tags: ['Food'] }
    ];

    const tagsContainer = document.getElementById('tagsContainer');
    const buttonsContainer = document.getElementById('buttonsContainer');
    const popup = document.getElementById('popup');
    const closePopup = document.getElementById('closePopup');

    const tags = ['All', 'E-Commerce', 'Fashion', 'Food', 'Movie', 'Gaming', 'Trip', 'Other'];
    tags.forEach(tag => {
        const button = document.createElement('button');
        button.classList.add('TagButton');
        button.setAttribute('data-tag', tag.toLowerCase());
        button.textContent = tag;
        tagsContainer.appendChild(button);
    });

    const renderGiftCards = (filterTag) => {
        buttonsContainer.innerHTML = '';
        const filteredCards = filterTag === 'all' ? giftCards : giftCards.filter(card => card.tags.some(tag => tag.toLowerCase() === filterTag));
        filteredCards.forEach(card => {
            const button = document.createElement('button');
            button.classList.add('Btn');
            const img = document.createElement('img');
            img.src = card.image || '';
            img.alt = card.name;
            if (!card.image) {
                img.style.display = 'none';
                const name = document.createElement('div');
                name.textContent = card.name;
                button.appendChild(name);
            } else {
                button.appendChild(img);
            }
            const hr = document.createElement('hr');
            button.appendChild(hr);
            const discountText = document.createElement('div');
            discountText.classList.add('discount');
            discountText.textContent = `Discount: ${card.discount}`;
            button.appendChild(discountText);
            button.addEventListener('click', () => {
                document.getElementById('minLimit').textContent = `${card.min} ₹`;
                document.getElementById('discountValue').textContent = `${card.discount}`;
                const inputAmount = document.getElementById('inputAmount');
                const toBuyAmount = document.getElementById('toBuyAmount');
                const youPayAmount = document.getElementById('youPayAmount');
                const profitAmount = document.getElementById('profitAmount');
                inputAmount.min = card.min;
                inputAmount.max = MAX_ALL;
                inputAmount.placeholder = "Add a custom value";
                inputAmount.value = '';
                const calculateAmounts = (value) => {
                    const toPay = value - (value * parseFloat(card.discount) / 100);
                    const profit = value - toPay;
                    toBuyAmount.textContent = `${value} ₹`;
                    youPayAmount.textContent = `${toPay.toFixed(2)} ₹`;
                    profitAmount.textContent = `${profit.toFixed(2)} ₹`;
                };
                inputAmount.addEventListener('input', (e) => {
                    const value = parseInt(e.target.value);
                    if (value >= card.min && value <= MAX_ALL) {
                        calculateAmounts(value);
                    }
                });
                popup.style.display = 'flex';
            });
            buttonsContainer.appendChild(button);
        });
    };

    renderGiftCards('all');

    tagsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('TagButton')) {
            const tag = e.target.getAttribute('data-tag');
            renderGiftCards(tag);
            document.querySelectorAll('.TagButton').forEach(btn => btn.classList.remove('selected'));
            e.target.classList.add('selected');
        }
    });

    closePopup.addEventListener('click', () => {
        popup.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === popup) {
            popup.style.display = 'none';
        }
    });
});
