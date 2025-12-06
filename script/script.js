function handleSubmit(event) {
    event.preventDefault();

    // Get form values
    const username = event.target.querySelector('input[type="text"]').value;
    const password = event.target.querySelector('input[type="password"]').value;
    const rememberMe = event.target.querySelector('input[type="checkbox"]').checked;

    // ke backend
    console.log('Login attempt:', {
        username: username,
        password: password,
        rememberMe: rememberMe
    });

    alert('Login functionality would be implemented here!');
}

// package page

function showPackage(packageType) {
    // Hide all package contents
    const contents = document.querySelectorAll('.package-content');
    contents.forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected package content
    document.getElementById(packageType).classList.add('active');

    // Add active class to clicked tab
    event.target.classList.add('active');

    // Smooth scroll to content
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}