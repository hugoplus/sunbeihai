// Icon change function
function changeIcon() {
    chevronIcon = document.getElementById("chevronIcon");

    if (chevronIcon.classList.contains('bi-chevron-down')) {
        chevronIcon.classList.remove('bi-chevron-down');
        chevronIcon.classList.add('bi-chevron-up');
    } else {
        chevronIcon.classList.remove('bi-chevron-up');
        chevronIcon.classList.add('bi-chevron-down');
    }
};

// Email validation function
function isValidEmail(email) {
    // Regular expression for email validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("comment_form").addEventListener("submit", function(event) {
        const emailInput = document.getElementById("email");
        const emailValue = emailInput.value.trim();

        if (!isValidEmail(emailValue)) {
            event.preventDefault(); // Prevent form submission

            // Change border color to yellow for invalid email
            emailInput.classList.add("border");
            emailInput.classList.add("border-warning");
        }
    });

    document.getElementById("comment_trigger_button").addEventListener("click", changeIcon);
});