// auth.js - Handle authentication state on frontend

document.addEventListener('DOMContentLoaded', function() {
    // Small delay to ensure all DOM elements are loaded
    setTimeout(checkAuthState, 100);
});

function checkAuthState() {
    const currentUser = localStorage.getItem('currentUser');
    console.log('Checking auth state. Current user found:', !!currentUser);

    if (currentUser) {
        try {
            const user = JSON.parse(currentUser);
            console.log('User parsed successfully:', user);
            showAuthenticatedState(user);
        } catch (error) {
            console.error('Error parsing user data:', error);
            showUnauthenticatedState();
        }
    } else {
        console.log('No current user found, showing unauthenticated state');
        showUnauthenticatedState();
    }
}

function showAuthenticatedState(user) {
    console.log('Showing authenticated state for user:', user);

    // Hide login/signup buttons
    const buttonSU_SI = document.getElementById('buttonSU_SI');
    if (buttonSU_SI) {
        buttonSU_SI.style.display = 'none';
    }

    // Show user profile
    const userProfile = document.getElementById('userProfile');
    if (userProfile) {
        userProfile.style.display = 'flex';
        const userName = document.getElementById('userName');
        if (userName) {
            userName.textContent = user.name || user.email;
        }
    }

    // Show recommendation section
    const recommendationSection = document.getElementById('recommendationSection');
    if (recommendationSection) {
        console.log('Found recommendation section, showing it');
        recommendationSection.style.display = 'block';
        recommendationSection.style.visibility = 'visible';
    } else {
        console.error('Recommendation section not found!');
    }
}

function showUnauthenticatedState() {
    // Show login/signup buttons
    const buttonSU_SI = document.getElementById('buttonSU_SI');
    if (buttonSU_SI) {
        buttonSU_SI.style.display = 'flex';
    }

    // Hide user profile
    const userProfile = document.getElementById('userProfile');
    if (userProfile) {
        userProfile.style.display = 'none';
    }

    // Hide recommendation section
    const recommendationSection = document.getElementById('recommendationSection');
    if (recommendationSection) {
        recommendationSection.style.display = 'none';
    }
}

function logout() {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('rememberMe');
    window.location.href = './login.html';
}

function goToProfile() {
    window.location.href = './profile.html';
}

// Make these functions global for onclick handlers
window.logout = logout;
window.goToProfile = goToProfile;

// Test function to verify authentication state
function verifyAuthSetup() {
    console.log('=== AUTHENTICATION VERIFICATION ===');

    const currentUser = localStorage.getItem('currentUser');
    console.log('User in localStorage:', !!currentUser);

    if (currentUser) {
        const user = JSON.parse(currentUser);
        console.log('User data:', user);

        // Check if all elements are properly shown/hidden
        const buttonSU_SI = document.getElementById('buttonSU_SI');
        const userProfile = document.getElementById('userProfile');
        const recommendationSection = document.getElementById('recommendationSection');

        console.log('Login/signup buttons hidden:', buttonSU_SI ? buttonSU_SI.style.display === 'none' : 'not found');
        console.log('User profile shown:', userProfile ? userProfile.style.display === 'flex' : 'not found');
        console.log('Recommendation section shown:', recommendationSection ? recommendationSection.style.display === 'block' : 'not found');

        if (!recommendationSection || recommendationSection.style.display === 'none') {
            console.warn('Recommendation section is not visible! Forcing display...');
            if (recommendationSection) {
                recommendationSection.style.display = 'block';
                recommendationSection.style.visibility = 'visible';
                recommendationSection.style.opacity = '1';
            }
        }
    } else {
        console.log('No user authenticated');
    }

    console.log('=== END VERIFICATION ===');
}

// Run verification after a delay to ensure DOM is ready
setTimeout(verifyAuthSetup, 500);