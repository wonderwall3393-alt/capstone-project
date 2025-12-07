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

function showPackage(packageType) {
    const contents = document.querySelectorAll('.package-content');
    contents.forEach(content => {
        content.classList.remove('active');
    });

    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(packageType).classList.add('active');
    event.target.classList.add('active');
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// package script

function selectPackage(quota, validity, price) {
    const paymentUrl = `payment.html?quota=${encodeURIComponent(quota)}&validity=${encodeURIComponent(validity)}&price=${encodeURIComponent(price)}`;
    window.location.href = paymentUrl;
}

document.addEventListener('DOMContentLoaded', function () {
    const packageCards = document.querySelectorAll('.package-card');

    packageCards.forEach(card => {
        card.style.cursor = 'pointer';

        card.addEventListener('click', function () {
            const quota = this.querySelector('.quota').textContent;
            const validity = this.querySelector('.validity').textContent;
            const priceElement = this.querySelector('.price');
            const price = priceElement.textContent;

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
});

// payment script

let selectedPaymentType = null;
let selectedPaymentProvider = null;

function getPackageData() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('quota')) {
        document.getElementById('packageQuota').textContent = params.get('quota');
        document.getElementById('packageValidity').textContent = params.get('validity');
        document.getElementById('totalPrice').textContent = params.get('price');
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

    document.getElementById('bankOptions').style.display = 'none';
    document.getElementById('ewalletOptions').style.display = 'none';
    document.getElementById('paymentDetails').style.display = 'none';

    if (type === 'bank') {
        document.getElementById('paymentBank').checked = true;
        document.querySelector('[onclick="selectPaymentMethod(\'bank\')"]').classList.add('selected');
        document.getElementById('bankOptions').style.display = 'grid';
    } else if (type === 'ewallet') {
        document.getElementById('paymentEwallet').checked = true;
        document.querySelector('[onclick="selectPaymentMethod(\'ewallet\')"]').classList.add('selected');
        document.getElementById('ewalletOptions').style.display = 'grid';
    }

    updatePayButton();
}

function selectBank(bank) {
    selectedPaymentProvider = bank;
    document.querySelectorAll('.bank-option').forEach(option => {
        option.classList.remove('selected');
    });
    event.target.closest('.bank-option').classList.add('selected');

    showPaymentDetails(bank, 'bank');
    updatePayButton();
}

function selectEwallet(ewallet) {
    selectedPaymentProvider = ewallet;
    document.querySelectorAll('.ewallet-option').forEach(option => {
        option.classList.remove('selected');
    });
    event.target.closest('.ewallet-option').classList.add('selected');

    showPaymentDetails(ewallet, 'ewallet');
    updatePayButton();
}

function showPaymentDetails(provider, type) {
    const detailsDiv = document.getElementById('paymentDetails');
    const instructionsP = document.getElementById('paymentInstructions');

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
    const phone = document.getElementById('phoneNumber').value;
    const btnPay = document.getElementById('btnPay');

    if (selectedPaymentType && selectedPaymentProvider && phone.length >= 10) {
        btnPay.disabled = false;
    } else {
        btnPay.disabled = true;
    }
}

function processPayment() {
    const phone = document.getElementById('phoneNumber').value;

    if (!phone || phone.length < 10) {
        alert('Mohon masukkan nomor telepon yang valid');
        return;
    }

    if (!selectedPaymentType || !selectedPaymentProvider) {
        alert('Mohon pilih metode pembayaran');
        return;
    }

    const btnPay = document.getElementById('btnPay');
    btnPay.textContent = 'Memproses...';
    btnPay.disabled = true;

    setTimeout(() => {
        document.getElementById('successModal').classList.add('active');
    }, 1500);
}

function cancelPayment() {
    if (confirm('Apakah Anda yakin ingin membatalkan pembayaran?')) {
        window.history.back();
    }
}

function closeModal() {
    window.location.href = 'home-before.html';
}

document.getElementById('phoneNumber').addEventListener('input', updatePayButton);

getPackageData();