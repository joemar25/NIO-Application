const menuOpenButton = document.querySelector('.menu-open-button');
const menu = document.querySelector('.menu');
const menuOpenCheckbox = document.querySelector('.menu-open');

// add click event listener to the document
document.addEventListener('click', (event) => {
    // check if the clicked element is inside the menu
    if (!menu.contains(event.target) && menuOpenCheckbox.checked) {
        // set the checked property to false to close the menu
        menuOpenCheckbox.checked = false;
    }
});

// add click event listener to the menu open button
menuOpenButton.addEventListener('click', (event) => {
    // stop the event from bubbling up to the document
    event.stopPropagation();
});