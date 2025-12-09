// signup.js - Logic untuk Sign-up/Register Sphinx Net

// Check if user is already logged in
window.addEventListener("DOMContentLoaded", () => {
  const currentUser = localStorage.getItem("currentUser");
  if (currentUser) {
    window.location.href = "./beranda.html";
  }
});

// Handle form submission
document
  .getElementById("signUpForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value;
    const passwordConfirm = document.getElementById("passwordConfirm").value;
    const termsAccepted = document.getElementById("terms").checked;
    const signupBtn = document.querySelector(".btn-signup");

    // Clear previous messages
    clearMessages();

    // Validate passwords match
    if (password !== passwordConfirm) {
      showError("Passwords do not match!");
      return;
    }

    // Validate username length
    if (username.length < 6) {
      showError("Username must be at least 6 characters!");
      return;
    }

    // Validate password length
    if (password.length < 8) {
      showError("Password must be at least 8 characters!");
      return;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      showError("Please enter a valid email address!");
      return;
    }

    // Validate phone number
    const phoneRegex = /^[0-9]{10,15}$/;
    if (!phoneRegex.test(phone.replace(/[-\s]/g, ""))) {
      showError("Phone number must be 10-15 digits!");
      return;
    }

    // Validate terms
    if (!termsAccepted) {
      showError("You must agree to the Terms & Conditions!");
      return;
    }

    // Show loading state
    signupBtn.disabled = true;
    signupBtn.textContent = "Creating Account...";

    try {
      // Try to connect to backend API
      const response = await fetch("http://localhost:8000/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: username,
          email: email,
          phone: phone,
          password: password,
        }),
      });

      const result = await response.json();

      if (result.success) {
        // Store user data in localStorage
        localStorage.setItem('currentUser', JSON.stringify(result.user));

        showSuccess("Account created successfully! Redirecting...");
        setTimeout(() => {
          window.location.href = "./beranda.html";
        }, 2000);
      } else {
        showError(result.error || "Registration failed. Please try again.");
        signupBtn.disabled = false;
        signupBtn.textContent = "Daftar";
      }
    } catch (error) {
      console.error("Registration error:", error);

      // Fallback to demo mode
      handleDemoRegistration(username, email, phone, password, signupBtn);
    }
  });

// Demo registration handler (for testing without backend)
function handleDemoRegistration(username, email, phone, password, signupBtn) {
  setTimeout(() => {
    // Check if user already exists
    const existingUsers = JSON.parse(localStorage.getItem("demoUsers") || "[]");

    const userExists = existingUsers.some(
      (user) => user.email === email || user.username === username
    );

    if (userExists) {
      showError("User with this email or username already exists!");
      signupBtn.disabled = false;
      signupBtn.textContent = "Sign Up";
      return;
    }

    // Create new user
    const newUser = {
      id: Date.now(),
      username: username,
      email: email,
      phone: phone,
      password: password, // In production, NEVER store plain passwords!
      createdAt: new Date().toISOString(),
    };

    // Save to localStorage
    existingUsers.push(newUser);
    localStorage.setItem("demoUsers", JSON.stringify(existingUsers));

    // Show success message
    showSuccess("Account created successfully! Redirecting to login...");

    // Redirect to login page
    setTimeout(() => {
      window.location.href = "./login.html";
    }, 2000);
  }, 1000);
}

// Show error message
function showError(message) {
  const messageDiv = document.getElementById("messageBox");
  if (!messageDiv) {
    createMessageBox();
    return showError(message);
  }

  messageDiv.textContent = message;
  messageDiv.className = "message-box error-message";
  messageDiv.style.display = "block";

  // Auto hide after 5 seconds
  setTimeout(() => {
    messageDiv.style.display = "none";
  }, 5000);
}

// Show success message
function showSuccess(message) {
  const messageDiv = document.getElementById("messageBox");
  if (!messageDiv) {
    createMessageBox();
    return showSuccess(message);
  }

  messageDiv.textContent = message;
  messageDiv.className = "message-box success-message";
  messageDiv.style.display = "block";
}

// Clear all messages
function clearMessages() {
  const messageDiv = document.getElementById("messageBox");
  if (messageDiv) {
    messageDiv.style.display = "none";
    messageDiv.className = "message-box";
    messageDiv.textContent = "";
  }
}

// Create message box if not exists
function createMessageBox() {
  const form = document.getElementById("signUpForm");
  const messageDiv = document.createElement("div");
  messageDiv.id = "messageBox";
  messageDiv.className = "message-box";
  messageDiv.style.display = "none";
  form.parentNode.insertBefore(messageDiv, form);
}
