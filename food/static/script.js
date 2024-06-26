// static/your_app/script.js
document.addEventListener('DOMContentLoaded', (event) => {
    const ingredientInput = document.getElementById('ingredientInput');
    const dropdown = document.getElementById('ingredientDropdown');
    const addIngredientButton = document.getElementById('addIngredientButton');
    const allIngredients = document.querySelectorAll('#allIngredients .hidden-item');

    // Function to show/hide dropdown items based on input
    const filterDropdown = () => {
        const filter = ingredientInput.value.toLowerCase();
        dropdown.innerHTML = '';
        let count = 0;

        allIngredients.forEach(item => {
            const text = item.getAttribute('data-name').toLowerCase();
            if (text.includes(filter) && count < 7) {
                const newItem = document.createElement('li');
                newItem.className = 'dropdown-item';
                newItem.setAttribute('data-name', item.getAttribute('data-name'));
                newItem.textContent = item.getAttribute('data-name');
                dropdown.appendChild(newItem);
                count++;
            }
        });

        dropdown.style.display = count > 0 ? 'block' : 'none';
    };

    // Event listener for input field to filter dropdown items
    ingredientInput.addEventListener('keyup', () => {
        filterDropdown();
    });

    // Event listener for clicking on a dropdown item
    dropdown.addEventListener('click', (event) => {
        if (event.target && event.target.matches('li.dropdown-item')) {
            ingredientInput.value = event.target.getAttribute('data-name');
            dropdown.style.display = 'none';  // Hide dropdown after selection
        }
    });
});
