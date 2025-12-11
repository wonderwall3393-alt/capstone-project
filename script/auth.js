// auth.js - Handle authentication state on frontend

document.addEventListener('DOMContentLoaded', function () {
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

let usageChart = null;

document.addEventListener('DOMContentLoaded', function () {
    loadUserProfile();
    setTimeout(() => {
        loadCircularDiagram();
        loadUsageChart();
    }, 300);
});

function loadUserProfile() {
    const currentUser = localStorage.getItem('currentUser');

    if (!currentUser) {
        // Only redirect if we're on a page that requires authentication
        if (window.location.pathname.includes('profile.html')) {
            window.location.href = './login.html';
        }
        return;
    }

    const user = JSON.parse(currentUser);

    // Set user avatar (only if on profile page)
    const avatar = document.getElementById('profileAvatar');
    if (avatar) {
        const firstLetter = (user.name || user.email || 'U').charAt(0).toUpperCase();
        avatar.innerHTML = firstLetter;
    }

    // Set user information (only if elements exist)
    const userNameDisplay = document.getElementById('userNameDisplay');
    if (userNameDisplay) {
        userNameDisplay.textContent = user.name || user.email;
    }

    const userEmail = document.getElementById('userEmail');
    if (userEmail) {
        userEmail.textContent = user.email;
    }

    const userPhone = document.getElementById('userPhone');
    if (userPhone) {
        userPhone.textContent = user.phone || 'Belum diisi';
    }

    // Set member since date (only if element exists)
    if (user.created_at) {
        const date = new Date(user.created_at);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        document.getElementById('memberSince').textContent = 'Member sejak ' + date.toLocaleDateString('id-ID', options);
    } else {
        document.getElementById('memberSince').textContent = 'Member sejak baru saja';
    }
}

function loadCircularDiagram() {
    // Get package data from sessionStorage
    const quota = sessionStorage.getItem('packageQuota') || '0 GB';

    // Parse quota value
    let quotaValue = 0;
    if (quota.includes('GB')) {
        quotaValue = parseInt(quota);
    } else if (quota.includes('Mbps')) {
        quotaValue = parseInt(quota) * 5;
    } else if (quota === 'Unlimited') {
        quotaValue = 100;
    }

    // Calculate percentages based on quota
    const internetPercent = Math.min((quotaValue / 100) * 100, 100);
    const appsPercent = Math.min((quotaValue / 100) * 80, 100);
    const callsPercent = Math.min((quotaValue / 100) * 60, 100);
    const smsPercent = Math.min((quotaValue / 100) * 40, 100);

    // Update circles with animation
    updateCircle('circleInternet', internetPercent);
    updateCircle('circleApps', appsPercent);
    updateCircle('circleCalls', callsPercent);
    updateCircle('circleSms', smsPercent);

    // Update stat values
    document.getElementById('internetQuota').textContent = quota;
    document.getElementById('appsQuota').textContent = quota.includes('GB') ? (quotaValue * 0.8).toFixed(0) + ' GB' : quota;
    document.getElementById('callsQuota').textContent = (quotaValue * 10) + ' Min';
    document.getElementById('smsQuota').textContent = (quotaValue * 5) + ' SMS';

    // Show current package if exists
    if (quotaValue > 0) {
        const validity = sessionStorage.getItem('packageValidity') || '30 Hari';
        const price = sessionStorage.getItem('packagePrice') || 'Rp0';

        const packageSection = document.getElementById('currentPackageSection');
        packageSection.style.display = 'block';
        document.getElementById('packageName').textContent = quota + ' - ' + validity;
        document.getElementById('packageDetails').textContent = price;
    }
}

function updateCircle(circleId, percentage) {
    const circle = document.getElementById(circleId);
    const radius = parseFloat(circle.getAttribute('r'));
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (percentage / 100) * circumference;

    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = offset;
}

function loadUsageChart() {
    const ctx = document.getElementById('usageChart').getContext('2d');

    // Get package data from sessionStorage
    const quota = sessionStorage.getItem('packageQuota');

    let labels = [];
    let data = [];
    let backgroundColor = [];

    if (quota && quota !== '0 GB') {
        // Determine chart data based on package type
        if (quota.includes('GB') || quota.includes('Mbps') || quota === 'Unlimited') {
            labels = ['Streaming', 'Browsing', 'Gaming', 'Social Media', 'Lainnya'];
            data = [30, 25, 20, 15, 10];
            backgroundColor = ['#EB3F3F', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'];
        } else {
            labels = ['Streaming', 'Browsing', 'Gaming', 'Social Media', 'Lainnya'];
            data = [30, 25, 20, 15, 10];
            backgroundColor = ['#EB3F3F', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'];
        }
    } else {
        labels = ['Belum Ada', 'Data', 'Penggunaan', 'Tersedia', '-'];
        data = [20, 20, 20, 20, 20];
        backgroundColor = ['#E0E0E0', '#BDBDBD', '#9E9E9E', '#757575', '#616161'];
    }

    // Create chart with animation
    usageChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Penggunaan',
                data: data,
                backgroundColor: backgroundColor,
                borderWidth: 3,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 2000,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            family: 'Inter',
                            size: 13
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        family: 'Inter'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Inter'
                    },
                    callbacks: {
                        label: function (context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            }
        }
    });
}

function logout() {
    if (confirm('Apakah Anda yakin ingin keluar?')) {
        localStorage.removeItem('currentUser');
        sessionStorage.clear();
        window.location.href = './login.html';
    }
}