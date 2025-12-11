function handleSubmit(event) {
    event.preventDefault();

    const username = event.target.querySelector('input[type="text"]').value;
    const password = event.target.querySelector('input[type="password"]').value;
    const rememberMe = event.target.querySelector('input[type="checkbox"]').checked;

    console.log('Login attempt:', {
        username: username,
        password: password,
        rememberMe: rememberMe
    });

    alert('Login functionality would be implemented here!');
}

/// Global variable untuk menyimpan data paket
let packageData = null;

// Load data paket dari JSON
async function loadPackageData() {
    try {
        const response = await fetch('./data/packages.json');
        if (!response.ok) {
            throw new Error('Failed to load package data');
        }
        packageData = await response.json();
        renderPackages();
    } catch (error) {
        console.error('Error loading package data:', error);
        showErrorMessage();
    }
}

// Fungsi untuk menampilkan error message
function showErrorMessage() {
    const containers = ['quota', 'sim-credit', 'wifi'];
    containers.forEach(containerId => {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">
                    <p>Gagal memuat data paket. Silakan refresh halaman.</p>
                </div>
            `;
        }
    });
}

// Fungsi untuk render semua paket
function renderPackages() {
    if (!packageData) return;

    const quotaContainer = document.getElementById('quota');
    if (quotaContainer && packageData.quota) {
        quotaContainer.innerHTML = '';
        packageData.quota.forEach(section => {
            quotaContainer.innerHTML += createSection(section);
        });
    }

    const simCreditContainer = document.getElementById('sim-credit');
    if (simCreditContainer && packageData.simCredit) {
        simCreditContainer.innerHTML = '';
        packageData.simCredit.forEach(section => {
            simCreditContainer.innerHTML += createSection(section);
        });
    }

    const wifiContainer = document.getElementById('wifi');
    if (wifiContainer && packageData.wifi) {
        wifiContainer.innerHTML = '';
        packageData.wifi.forEach(section => {
            wifiContainer.innerHTML += createSection(section);
        });
    }

    attachCardEventListeners();
}

// Fungsi untuk membuat section HTML
function createSection(section) {
    const cardsHtml = section.packages.map(pkg => createCard(pkg)).join('');

    return `
        <div class="promo-section">
            <div class="section-header">
                <div class="section-title">${section.sectionTitle}</div>
                <div class="view-all">Lihat Semua</div>
            </div>
            <div class="cards-container">
                ${cardsHtml}
            </div>
        </div>
    `;
}

// Fungsi untuk membuat card HTML
function createCard(pkg) {
    const nameHtml = pkg.name ? `<div class="package-name">${pkg.name}</div>` : '';
    const oldPriceHtml = pkg.oldPrice ? `<div class="old-price">${pkg.oldPrice}</div>` : '';
    const extraHtml = pkg.extra ? `<div class="price-per-gb">${pkg.extra}</div>` : '';

    return `
        <div class="package-card" data-quota="${pkg.quota}" data-validity="${pkg.validity}" data-price="${pkg.price}">
            ${nameHtml}
            <div class="quota">${pkg.quota}</div>
            <div class="validity">${pkg.validity}</div>
            ${oldPriceHtml}
            <div class="price">${pkg.price}</div>
            ${extraHtml}
        </div>
    `;
}

// Fungsi untuk attach event listeners ke cards
function attachCardEventListeners() {
    const packageCards = document.querySelectorAll('.package-card');

    packageCards.forEach(card => {
        card.style.cursor = 'pointer';

        card.addEventListener('click', function () {
            const quota = this.dataset.quota || this.querySelector('.quota').textContent;
            const validity = this.dataset.validity || this.querySelector('.validity').textContent;
            const price = this.dataset.price || this.querySelector('.price').textContent;

            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
                selectPackage(quota, validity, price);
            }, 150);
        });

        card.addEventListener('mouseenter', function () {
            this.style.boxShadow = '0 8px 20px rgba(235, 63, 63, 0.2)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.boxShadow = '';
        });
    });
}

// Fungsi untuk menampilkan paket berdasarkan tipe
function showPackage(packageType) {
    const contents = document.querySelectorAll('.package-content');
    contents.forEach(content => {
        content.classList.remove('active');
    });

    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    const selectedContent = document.getElementById(packageType);
    if (selectedContent) {
        selectedContent.classList.add('active');
    }

    event.target.classList.add('active');

    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Fungsi untuk select package dan redirect ke payment
function selectPackage(quota, validity, price) {
    const paymentUrl = `payment.html?quota=${encodeURIComponent(quota)}&validity=${encodeURIComponent(validity)}&price=${encodeURIComponent(price)}`;
    window.location.href = paymentUrl;
}

// Payment Page Functions
let selectedPaymentType = null;
let selectedPaymentProvider = null;

function getPackageData() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('quota')) {
        const quotaElement = document.getElementById('packageQuota');
        const validityElement = document.getElementById('packageValidity');
        const priceElement = document.getElementById('totalPrice');

        if (quotaElement) quotaElement.textContent = params.get('quota');
        if (validityElement) validityElement.textContent = params.get('validity');
        if (priceElement) priceElement.textContent = params.get('price');
    }
}

function selectPaymentMethod(type) {
    selectedPaymentType = type;
    selectedPaymentProvider = null;

    document.querySelectorAll('.payment-method').forEach(method => {
        method.classList.remove('selected');
    });
    document.querySelectorAll('.bank-option, .ewallet-option').forEach(option => {
        option.classList.remove('selected');
    });

    const bankOptions = document.getElementById('bankOptions');
    const ewalletOptions = document.getElementById('ewalletOptions');
    const paymentDetails = document.getElementById('paymentDetails');

    if (bankOptions) bankOptions.style.display = 'none';
    if (ewalletOptions) ewalletOptions.style.display = 'none';
    if (paymentDetails) paymentDetails.style.display = 'none';

    if (type === 'bank') {
        const bankRadio = document.getElementById('paymentBank');
        if (bankRadio) bankRadio.checked = true;

        const bankMethod = document.querySelector('[onclick="selectPaymentMethod(\'bank\')"]');
        if (bankMethod) bankMethod.classList.add('selected');
        if (bankOptions) bankOptions.style.display = 'grid';
    } else if (type === 'ewallet') {
        const ewalletRadio = document.getElementById('paymentEwallet');
        if (ewalletRadio) ewalletRadio.checked = true;

        const ewalletMethod = document.querySelector('[onclick="selectPaymentMethod(\'ewallet\')"]');
        if (ewalletMethod) ewalletMethod.classList.add('selected');
        if (ewalletOptions) ewalletOptions.style.display = 'grid';
    }

    updatePayButton();
}

function selectBank(bank) {
    selectedPaymentProvider = bank;
    document.querySelectorAll('.bank-option').forEach(option => {
        option.classList.remove('selected');
    });
    if (event && event.target) {
        const target = event.target.closest('.bank-option');
        if (target) target.classList.add('selected');
    }

    showPaymentDetails(bank, 'bank');
    updatePayButton();
}

function selectEwallet(ewallet) {
    selectedPaymentProvider = ewallet;
    document.querySelectorAll('.ewallet-option').forEach(option => {
        option.classList.remove('selected');
    });
    if (event && event.target) {
        const target = event.target.closest('.ewallet-option');
        if (target) target.classList.add('selected');
    }

    showPaymentDetails(ewallet, 'ewallet');
    updatePayButton();
}

function showPaymentDetails(provider, type) {
    const detailsDiv = document.getElementById('paymentDetails');
    const instructionsP = document.getElementById('paymentInstructions');

    if (!detailsDiv || !instructionsP) return;

    if (type === 'bank') {
        const accountNumbers = {
            'BCA': '1234567890',
            'Mandiri': '0987654321',
            'BNI': '1122334455',
            'BRI': '5544332211'
        };
        instructionsP.innerHTML = `
            <strong>Transfer ke rekening ${provider}</strong><br>
            No. Rekening: <strong>${accountNumbers[provider]}</strong><br>
            a.n. PT Sphinx Net Indonesia<br><br>
            <em>Setelah transfer, konfirmasi pembayaran akan diproses otomatis.</em>
        `;
    } else {
        instructionsP.innerHTML = `
            <strong>Pembayaran via ${provider}</strong><br>
            Scan QR Code yang akan muncul setelah Anda klik "Bayar Sekarang"<br><br>
            <em>Pastikan saldo ${provider} Anda mencukupi.</em>
        `;
    }

    detailsDiv.style.display = 'block';
}

function updatePayButton() {
    const phoneInput = document.getElementById('phoneNumber');
    const btnPay = document.getElementById('btnPay');

    if (!phoneInput || !btnPay) return;

    const phone = phoneInput.value;

    if (selectedPaymentType && selectedPaymentProvider && phone.length >= 10) {
        btnPay.disabled = false;
    } else {
        btnPay.disabled = true;
    }
}

function processPayment() {
    const phoneInput = document.getElementById('phoneNumber');
    if (!phoneInput) return;

    const phone = phoneInput.value;

    if (!phone || phone.length < 10) {
        alert('Mohon masukkan nomor telepon yang valid');
        return;
    }

    if (!selectedPaymentType || !selectedPaymentProvider) {
        alert('Mohon pilih metode pembayaran');
        return;
    }

    // Ambil data paket dari URL params
    const params = new URLSearchParams(window.location.search);
    const quota = params.get('quota') || '15 GB';
    const validity = params.get('validity') || '30 Hari';
    const price = params.get('price') || 'Rp50.000';

    // Simpan semua data ke sessionStorage
    sessionStorage.setItem('paymentPhone', phone);
    sessionStorage.setItem('paymentType', selectedPaymentType);
    sessionStorage.setItem('paymentProvider', selectedPaymentProvider);
    sessionStorage.setItem('packageQuota', quota);
    sessionStorage.setItem('packageValidity', validity);
    sessionStorage.setItem('packagePrice', price);

    const btnPay = document.getElementById('btnPay');
    if (btnPay) {
        btnPay.textContent = 'Memproses...';
        btnPay.disabled = true;
    }

    // Redirect ke halaman proof setelah delay singkat
    setTimeout(() => {
        window.location.href = 'proof.html';
    }, 500);
}

function cancelPayment() {
    if (confirm('Apakah Anda yakin ingin membatalkan pembayaran?')) {
        window.history.back();
    }
}

function closeModal() {
    window.location.href = 'home-before.html';
}

// Initialize saat DOM ready
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('quota') || document.getElementById('sim-credit') || document.getElementById('wifi')) {
        loadPackageData();
    }

    const phoneInput = document.getElementById('phoneNumber');
    if (phoneInput) {
        phoneInput.addEventListener('input', updatePayButton);
        getPackageData();
    }
});

// ===== PROOF PAGE FUNCTIONS =====

// Generate transaction ID
function generateTransactionId() {
    const date = new Date();
    const dateStr = date.toISOString().slice(0, 10).replace(/-/g, '');
    const randomStr = Math.random().toString(36).substring(2, 7).toUpperCase();
    return `TRX-${dateStr}-${randomStr}`;
}

// Format date time
function formatDateTime() {
    const date = new Date();
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${day} ${month} ${year}, ${hours}:${minutes} WIB`;
}

// Load receipt data from sessionStorage
function loadReceiptData() {
    // Generate transaction ID
    const transactionIdEl = document.getElementById('transactionId');
    if (transactionIdEl) {
        transactionIdEl.textContent = generateTransactionId();
    }

    // Set date time
    const dateTimeEl = document.getElementById('dateTime');
    if (dateTimeEl) {
        dateTimeEl.textContent = formatDateTime();
    }

    // Ambil data dari sessionStorage
    const phone = sessionStorage.getItem('paymentPhone') || '08xxxxxxxxxx';
    const quota = sessionStorage.getItem('packageQuota') || '15 GB';
    const validity = sessionStorage.getItem('packageValidity') || '30 Hari';
    const price = sessionStorage.getItem('packagePrice') || 'Rp50.000';
    const paymentType = sessionStorage.getItem('paymentType') || 'bank';
    const paymentProvider = sessionStorage.getItem('paymentProvider') || 'BCA';

    // Set phone number
    const phoneNumberEl = document.getElementById('phoneNumber');
    if (phoneNumberEl) {
        phoneNumberEl.textContent = phone;
    }

    // Set package details
    const packageQuotaEl = document.getElementById('packageQuota');
    if (packageQuotaEl) {
        packageQuotaEl.textContent = quota;
    }

    const packageValidityEl = document.getElementById('packageValidity');
    if (packageValidityEl) {
        packageValidityEl.textContent = validity;
    }

    const totalAmountEl = document.getElementById('totalAmount');
    if (totalAmountEl) {
        totalAmountEl.textContent = price;
    }

    // Set payment method
    const paymentIconEl = document.getElementById('paymentIcon');
    const paymentMethodEl = document.getElementById('paymentMethod');
    const paymentAccountEl = document.getElementById('paymentAccount');

    if (paymentType === 'bank') {
        if (paymentIconEl) paymentIconEl.textContent = '🏦';
        if (paymentMethodEl) paymentMethodEl.textContent = `Transfer Bank ${paymentProvider}`;

        const accountNumbers = {
            'BCA': '1234567890',
            'Mandiri': '0987654321',
            'BNI': '1122334455',
            'BRI': '5544332211'
        };
        if (paymentAccountEl) {
            paymentAccountEl.textContent = `Rekening: ${accountNumbers[paymentProvider] || '1234567890'}`;
        }
    } else if (paymentType === 'ewallet') {
        if (paymentIconEl) paymentIconEl.textContent = '💳';
        if (paymentMethodEl) paymentMethodEl.textContent = paymentProvider;
        if (paymentAccountEl) paymentAccountEl.textContent = 'E-Wallet';
    }

    // Clear sessionStorage setelah data dimuat (opsional)
    // Uncomment jika ingin clear data setelah ditampilkan
    // sessionStorage.clear();
}

// Download receipt as PDF (for now just print)
function downloadReceipt() {
    window.print();
}

// Go to home page
function goToHome() {
    window.location.href = 'beranda.html';
}

// Load data when proof page loads
if (window.location.pathname.includes('proof.html')) {
    window.addEventListener('DOMContentLoaded', loadReceiptData);
}