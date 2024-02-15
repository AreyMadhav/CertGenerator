// Function to validate the login form
function validateLoginForm() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Perform validation (e.g., check if fields are not empty)
    if (username === '' || password === '') {
        alert('Please enter both username and password');
        return false;
    }
    return true;
}

// Function to handle AJAX request for logging in
function loginUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Example AJAX request using Fetch API
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Login successful');
            // Redirect to the main page or perform any other action
            window.location.href = '/index';
        } else {
            alert('Login failed. Please check your credentials');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request');
    });
}

// Add event listener for form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    if (validateLoginForm()) {
        loginUser();
    }
});
