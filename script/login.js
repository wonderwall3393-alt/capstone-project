// login.js - Logic untuk Login Sphinx Net

// Check if user is already logged in
window.addEventListener("DOMContentLoaded", () => {
  const currentUser = localStorage.getItem("currentUser");
  if (currentUser) {
    window.location.href = "./beranda.html";
  }
});

// Handle form submission
document
  .getElementById("loginForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const rememberMe = document.getElementById("rememberMe").checked;
    const loginBtn = document.getElementById("loginBtn");
    const errorMessage = document.getElementById("errorMessage");

    // Clear previous messages
    hideError();

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      showError("Please enter a valid email address!");
      return;
    }

    // Show loading state
    loginBtn.disabled = true;
    loginBtn.textContent = "Signing In...";

    try {
      // Try to connect to backend API
      const response = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const result = await response.json();

      if (result.success) {
        // Store user data in localStorage
        localStorage.setItem('currentUser', JSON.stringify(result.user));

        if (rememberMe) {
          localStorage.setItem('rememberMe', 'true');
        }

        showSuccess("Login successful! Redirecting...");
        setTimeout(() => {
          window.location.href = "./beranda.html";
        }, 1000);
      } else {
        showError(result.error || "Login failed. Please check your credentials.");
        loginBtn.disabled = false;
        loginBtn.textContent = "Masuk";
      }
    } catch (error) {
      console.error("Login error:", error);

      // Fallback to demo mode
      handleDemoLogin(email, password, loginBtn);
    }
  });

// Demo login handler (for testing without backend)
function handleDemoLogin(email, password, loginBtn) {
  setTimeout(() => {
    // Check if user exists in demo storage
    const existingUsers = JSON.parse(localStorage.getItem("demoUsers") || "[]");

    const user = existingUsers.find(
      (user) => user.email === email && user.password === password
    );

    if (user) {
      // Create user object for session
      const userSession = {
        id: user.id,
        name: user.username,
        email: user.email,
        phone: user.phone,
        package: null
      };

      localStorage.setItem('currentUser', JSON.stringify(userSession));

      showSuccess("Login successful! Redirecting...");
      setTimeout(() => {
        window.location.href = "./beranda.html";
      }, 1000);
    } else {
      showError("Invalid email or password!");
      loginBtn.disabled = false;
      loginBtn.textContent = "Masuk";
    }
  }, 1000);
}

// Show error message
function showError(message) {
  const errorMessage = document.getElementById("errorMessage");
  if (errorMessage) {
    errorMessage.textContent = message;
    errorMessage.className = "error-message show";
    errorMessage.style.display = "block";

    // Auto hide after 5 seconds
    setTimeout(() => {
      hideError();
    }, 5000);
  }
}

// Hide error message
function hideError() {
  const errorMessage = document.getElementById("errorMessage");
  if (errorMessage) {
    errorMessage.style.display = "none";
    errorMessage.className = "error-message";
  }
}

// Show success message
function showSuccess(message) {
  const errorMessage = document.getElementById("errorMessage");
  if (errorMessage) {
    errorMessage.textContent = message;
    errorMessage.className = "error-message success";
    errorMessage.style.display = "block";
  }
}