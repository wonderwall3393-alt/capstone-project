// Data Paket Internet
const packages = [
    { name: "Sphinx Stable 20GB", kuota: "20GB", harga: 40000, category: "stable" },
    { name: "Sphinx Stable 50GB", kuota: "50GB", harga: 75000, category: "stable" },
    { name: "Sphinx Stable 100GB", kuota: "100GB", harga: 120000, category: "stable" },
    { name: "Sphinx Hemat 5GB", kuota: "5GB", harga: 25000, category: "hemat" },
    { name: "Sphinx Hemat 10GB", kuota: "10GB", harga: 35000, category: "hemat" },
    { name: "Sphinx Hemat 20GB", kuota: "20GB", harga: 45000, category: "hemat" },
    { name: "Sphinx Hemat 30GB", kuota: "30GB", harga: 55000, category: "hemat" },
    { name: "Sphinx Unlimited", kuota: "Unlimited", harga: 250000, category: "unlimited" },
    { name: "Sphinx Call Pro", kuota: "300 Menit", harga: 50000, category: "call" },
    { name: "Sphinx Call Flex", kuota: "150 Menit", harga: 30000, category: "call" },
    { name: "Sphinx Call Lite", kuota: "60 Menit", harga: 15000, category: "call" },
    { name: "Sphinx Social 10GB", kuota: "10GB", harga: 20000, category: "social" },
    { name: "Sphinx Stream 50GB", kuota: "50GB", harga: 70000, category: "stream" },
    { name: "Sphinx Stream 100GB", kuota: "100GB", harga: 120000, category: "stream" },
    { name: "Sphinx Work Connect 30GB", kuota: "30GB", harga: 55000, category: "work" },
    { name: "Sphinx Gamer Pro 40GB", kuota: "40GB", harga: 65000, category: "gaming" },
    { name: "Sphinx Gamer Max 80GB", kuota: "80GB", harga: 110000, category: "gaming" },
    { name: "Sphinx IoT Home 20GB", kuota: "20GB", harga: 30000, category: "iot" },
    { name: "Sphinx IoT Fiber 30 Mbps", kuota: "Fiber IoT", harga: 150000, category: "iot" },
    { name: "Sphinx Global Lite", kuota: "1GB", harga: 75000, category: "roaming" },
    { name: "Sphinx Global Pass", kuota: "3GB", harga: 150000, category: "roaming" },
    { name: "Sphinx Roam Max", kuota: "10GB", harga: 350000, category: "roaming" }
];

// Survey Questions
const surveyQuestions = [
    {
        id: "phone_model",
        question: "Handphone apa yang Anda pakai?",
        type: "radio",
        options: [
            "iPhone (13/14/15 Pro Max)",
            "iPhone (12/13/14)",
            "iPhone (11/XS/XR)",
            "Samsung Galaxy S Series",
            "Samsung Galaxy A Series",
            "OPPO Reno/Find Series",
            "Xiaomi Redmi Note Series",
            "Xiaomi Mi/Poco Series",
            "Vivo V/S Series",
            "Realme GT/Pro Series",
            "Lainnya"
        ]
    },
    {
        id: "gender",
        question: "Apa jenis kelamin anda?",
        type: "radio",
        options: ["Laki-laki", "Perempuan"]
    },
    {
        id: "reason",
        question: "Apa alasan Anda memilih produk ini?",
        type: "radio",
        options: ["Mencari internet yang stabil", "Mencari internet yang murah", "Mencari paket unlimited"]
    },
    {
        id: "call_frequency",
        question: "Seberapa sering Anda menggunakan paket telepon?",
        type: "radio",
        options: ["Tidak pernah", "Jarang", "Kadang", "Sering"]
    },
    {
        id: "wifi",
        question: "Apakah anda memiliki wifi?",
        type: "radio",
        options: ["Ya dirumah", "Ya di kantor", "Tidak"]
    },
    {
        id: "housing",
        question: "Apa jenis hunian Anda?",
        type: "radio",
        options: ["Rumah pribadi", "Apartemen", "Kost/kontrakan"]
    },
    {
        id: "usage",
        question: "Untuk keperluan apa Anda menggunakan internet? (boleh pilih lebih dari satu)",
        type: "checkbox",
        options: [
            "Browsing & media sosial",
            "Streaming video (YouTube, Netflix, dll.)",
            "Video conference (Zoom, Teams, dll.)",
            "Gaming online",
            "Smart home / IoT"
        ]
    },
    {
        id: "quota",
        question: "Berapa estimasi penggunaan kuota internet per bulan?",
        type: "radio",
        options: ["< 10 GB", "10-25 GB", "25-50 GB", "50–100 GB", "100–300 GB", "> 300 GB / unlimited"]
    },
    {
        id: "budget",
        question: "Berapa anggaran bulanan Anda untuk internet?",
        type: "radio",
        options: ["< Rp25.000", "Rp25.000–Rp50.000", "Rp.50.000-Rp100.000", "Rp.100.000–Rp250.000", "> Rp250.000"]
    },
    {
        id: "preference",
        question: "Anda lebih suka jenis paket:",
        type: "radio",
        options: ["Unlimited", "Kuota besar", "Hemat/entry-level", "Paket bundling TV/telepon"]
    },
    {
        id: "roaming",
        question: "Apakah anda sering pergi ke luar negeri?",
        type: "radio",
        options: ["Tidak", "Jarang", "Kadang", "Sering"]
    }
];

// State
let currentQuestion = 0;
let surveyAnswers = {};

// Elements
const surveyBtn = document.getElementById('surveyBtn');
const surveyModal = document.getElementById('surveyModal');
const surveyQuestionsContainer = document.getElementById('surveyQuestions');
const btnPrev = document.getElementById('btnPrev');
const btnNext = document.getElementById('btnNext');
const btnSubmit = document.getElementById('btnSubmit');
const recommendationsContainer = document.getElementById('recommendationsContainer');
const recommendationCards = document.getElementById('recommendationCards');
const retakeBtn = document.getElementById('retakeBtn');

// Check if all survey elements exist
if (surveyBtn && surveyModal && surveyQuestionsContainer) {
    // Initialize Survey
    initSurvey();
} else {
    console.warn('Some survey elements not found:', {
        surveyBtn: !!surveyBtn,
        surveyModal: !!surveyModal,
        surveyQuestionsContainer: !!surveyQuestionsContainer
    });
}

// Initialize Survey
function initSurvey() {
    surveyQuestionsContainer.innerHTML = '';
    surveyQuestions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'survey-question';
        if (index === 0) questionDiv.classList.add('active');

        let optionsHTML = '';
        q.options.forEach((option, optIndex) => {
            const inputType = q.type;
            const inputName = q.id;
            const inputId = `${q.id}_${optIndex}`;
            optionsHTML += `
                <label class="option-label" for="${inputId}">
                    <input type="${inputType}" name="${inputName}" id="${inputId}" value="${option}">
                    <span>${option}</span>
                </label>
            `;
        });

        questionDiv.innerHTML = `
            <div class="question-number">Pertanyaan ${index + 1} dari ${surveyQuestions.length}</div>
            <div class="question-title">${q.question}</div>
            <div class="options-container">
                ${optionsHTML}
            </div>
        `;

        surveyQuestionsContainer.appendChild(questionDiv);
    });

    // Add event listeners for option selection
    document.querySelectorAll('.option-label input').forEach(input => {
        input.addEventListener('change', function() {
            if (this.type === 'radio') {
                document.querySelectorAll(`input[name="${this.name}"]`).forEach(radio => {
                    radio.closest('.option-label').classList.remove('selected');
                });
            }
            if (this.checked) {
                this.closest('.option-label').classList.add('selected');
            } else {
                this.closest('.option-label').classList.remove('selected');
            }
        });
    });
}

// Show Survey Modal
if (surveyBtn) {
    surveyBtn.addEventListener('click', (e) => {
        e.preventDefault();
        surveyModal.classList.add('active');
        currentQuestion = 0;
        surveyAnswers = {};
        initSurvey();
        updateButtons();
    });
}

// Close modal when clicking outside
if (surveyModal) {
    surveyModal.addEventListener('click', (e) => {
        if (e.target === surveyModal) {
            e.preventDefault();
            surveyModal.classList.remove('active');
        }
    });
}

// Prevent form submission
const surveyForm = document.getElementById('surveyForm');
if (surveyForm) {
    surveyForm.addEventListener('submit', (e) => {
        e.preventDefault();
        e.stopPropagation();
        return false;
    });
}

// Navigation
if (btnPrev) {
    btnPrev.addEventListener('click', (e) => {
        e.preventDefault();
        if (currentQuestion > 0) {
            saveCurrentAnswer();
            currentQuestion--;
            showQuestion(currentQuestion);
            updateButtons();
        }
    });
}

if (btnNext) {
    btnNext.addEventListener('click', (e) => {
        e.preventDefault();
        if (validateCurrentQuestion()) {
            saveCurrentAnswer();
            currentQuestion++;
            showQuestion(currentQuestion);
            updateButtons();
        } else {
            alert('Silakan pilih minimal satu jawaban');
        }
    });
}

if (btnSubmit) {
    btnSubmit.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (validateCurrentQuestion()) {
            saveCurrentAnswer();

            // Add phone model data to survey
            surveyAnswers.phone_model = document.querySelector('input[name="phone_model"]:checked')?.value;

            // Show loading state
            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Processing...';

            try {
                // Send data to Python backend
                const backendResult = await sendSurveyToPython(surveyAnswers);

                if (backendResult) {
                    displayRecommendations(backendResult.recommendations, backendResult.metadata);

                    // Submit survey to server for authenticated users
                    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
                    if (currentUser) {
                        await submitSurveyToServer(currentUser.id, surveyAnswers, backendResult.recommendations);
                    }
                } else {
                    // Fallback to frontend calculation
                    calculateRecommendations();
                }
            } catch (error) {
                console.error('Error processing recommendations:', error);
                // Fallback to frontend calculation
                calculateRecommendations();
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Submit';
                surveyModal.classList.remove('active');
                showRecommendations();
            }
        } else {
            alert('Silakan pilih minimal satu jawaban');
        }
    });
}

if (retakeBtn) {
    retakeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (surveyBtn) {
            surveyModal.classList.add('active');
            currentQuestion = 0;
            surveyAnswers = {};
            initSurvey();
            updateButtons();
        }
    });
}

function showQuestion(index) {
    const questions = document.querySelectorAll('.survey-question');
    questions.forEach((q, i) => {
        q.classList.remove('active');
        if (i === index) {
            q.classList.add('active');
        }
    });
}

function updateButtons() {
    btnPrev.disabled = currentQuestion === 0;

    if (currentQuestion === surveyQuestions.length - 1) {
        btnNext.style.display = 'none';
        btnSubmit.style.display = 'block';
    } else {
        btnNext.style.display = 'block';
        btnSubmit.style.display = 'none';
    }
}

function validateCurrentQuestion() {
    const currentQ = surveyQuestions[currentQuestion];
    const inputs = document.querySelectorAll(`input[name="${currentQ.id}"]:checked`);
    return inputs.length > 0;
}

function saveCurrentAnswer() {
    const currentQ = surveyQuestions[currentQuestion];
    if (currentQ.type === 'checkbox') {
        const checked = Array.from(document.querySelectorAll(`input[name="${currentQ.id}"]:checked`))
            .map(input => input.value);
        surveyAnswers[currentQ.id] = checked;
    } else {
        const checked = document.querySelector(`input[name="${currentQ.id}"]:checked`);
        if (checked) {
            surveyAnswers[currentQ.id] = checked.value;
        }
    }
}

// Recommendation Logic
function calculateRecommendations() {
    const weights = {
        usage: 0.30,
        budget: 0.25,
        need: 0.20,
        preference: 0.15,
        call: 0.10,
        roaming: 0.10
    };

    const scores = packages.map(pkg => {
        let score = 0;

        // Usage Match (0.30)
        score += calculateUsageMatch(pkg) * weights.usage;

        // Budget Fit (0.25)
        score += calculateBudgetFit(pkg) * weights.budget;

        // Need Match (0.20)
        score += calculateNeedMatch(pkg) * weights.need;

        // Preference Match (0.15)
        score += calculatePreferenceMatch(pkg) * weights.preference;

        // Call Frequency (0.10)
        score += calculateCallMatch(pkg) * weights.call;

        // Roaming (0.10)
        score += calculateRoamingMatch(pkg) * weights.roaming;

        return { ...pkg, score: score };
    });

    // Sort by score and get top 6
    const topRecommendations = scores
        .sort((a, b) => b.score - a.score)
        .filter(pkg => pkg.score > 0)
        .slice(0, 6);

    displayRecommendations(topRecommendations);
}

function calculateUsageMatch(pkg) {
    const usage = surveyAnswers.usage || [];
    let match = 0;

    if (usage.includes('Browsing & media sosial')) {
        if (['social', 'hemat', 'stable'].includes(pkg.category)) match = 1;
    }
    if (usage.includes('Streaming video (YouTube, Netflix, dll.)')) {
        if (pkg.category === 'stream' || pkg.name.includes('Stream') || pkg.name.includes('Stable 50GB')) match = 1;
    }
    if (usage.includes('Video conference (Zoom, Teams, dll.)')) {
        if (pkg.category === 'work' || pkg.category === 'stable') match = 1;
    }
    if (usage.includes('Gaming online')) {
        if (pkg.category === 'gaming') match = 1;
    }
    if (usage.includes('Smart home / IoT')) {
        if (pkg.category === 'iot') match = 1;
    }

    return match;
}

function calculateBudgetFit(pkg) {
    const budgetMap = {
        "< Rp25.000": 25000,
        "Rp25.000–Rp50.000": 50000,
        "Rp.50.000-Rp100.000": 100000,
        "Rp.100.000–Rp250.000": 250000,
        "> Rp250.000": 500000
    };

    const userBudget = budgetMap[surveyAnswers.budget] || 100000;

    if (pkg.harga > userBudget) {
        const over = (pkg.harga - userBudget) / userBudget;
        return Math.max(0, 1 - over);
    }
    return 1;
}

function calculateNeedMatch(pkg) {
    const reason = surveyAnswers.reason;

    if (reason === "Mencari internet yang stabil" && pkg.category === "stable") return 1;
    if (reason === "Mencari internet yang murah" && pkg.category === "hemat") return 1;
    if (reason === "Mencari paket unlimited" && pkg.category === "unlimited") return 1;

    return 0;
}

function calculatePreferenceMatch(pkg) {
    const pref = surveyAnswers.preference;

    if (pref === "Unlimited" && pkg.category === "unlimited") return 1;
    if (pref === "Kuota besar" && (pkg.kuota.includes('50GB') || pkg.kuota.includes('100GB') || pkg.kuota.includes('80GB'))) return 1;
    if (pref === "Hemat/entry-level" && pkg.category === "hemat") return 1;
    if (pref === "Paket bundling TV/telepon" && pkg.category === "call") return 1;

    return 0.5;
}

function calculateCallMatch(pkg) {
    const callFreq = surveyAnswers.call_frequency?.toLowerCase() || "tidak pernah";

    if (pkg.category !== 'call') return 0;

    if (callFreq === "tidak pernah") return 0;
    if (callFreq === "jarang") return 0.3;
    if (callFreq === "kadang") return 0.6;
    if (callFreq === "sering") return 1;

    return 0;
}

function calculateRoamingMatch(pkg) {
    const roaming = surveyAnswers.roaming?.toLowerCase() || "tidak";

    if (pkg.category !== 'roaming') return 0;

    if (roaming === "tidak") return 0;
    if (roaming === "jarang") return 0.3;
    if (roaming === "kadang") return 0.6;
    if (roaming === "sering") return 1;

    return 0;
}

function displayRecommendations(recommendations, metadata = null) {
    recommendationCards.innerHTML = '';

    if (!recommendations || recommendations.length === 0) {
        recommendationCards.innerHTML = '<div class="no-recommendations">Tidak ada rekomendasi yang sesuai. Silakan coba lagi dengan jawaban berbeda.</div>';
        return;
    }

    // Count AI Model and Survey recommendations
    const aiCount = recommendations.filter(pkg => pkg.recommendation_type === 'ml_model').length;
    const surveyCount = recommendations.filter(pkg => pkg.recommendation_type === 'survey_based').length;

    // Add header showing recommendation types
    const headerDiv = document.createElement('div');
    headerDiv.className = 'recommendation-header';
    headerDiv.innerHTML = `
        <h2>Rekomendasi Untuk Anda</h2>
        <div class="recommendation-stats">
            <div class="stat-item ai-stat">
                <i class="fa-solid fa-brain"></i>
                <span>AI Model: ${aiCount} paket</span>
            </div>
            <div class="stat-item survey-stat">
                <span>Survey Analysis: ${surveyCount} paket</span>
            </div>
        </div>
        <div class="recommendation-subtitle">Total ${recommendations.length} rekomendasi ditemukan</div>
    `;
    recommendationCards.appendChild(headerDiv);

    // Create recommendation cards container
    const cardsContainer = document.createElement('div');
    cardsContainer.className = 'recommendation-cards-contrainer';

    // Add all recommendation cards with clear labels
    recommendations.forEach(pkg => {
        const isAI = pkg.recommendation_type === 'ml_model';
        const matchPercentage = pkg.match_percentage || Math.round((pkg.score || 0) * 100);

        const cardHTML = createHybridRecommendationCard(pkg, isAI, matchPercentage);
        cardsContainer.innerHTML += cardHTML;
    });

    recommendationCards.appendChild(cardsContainer);
}

function createHybridRecommendationCard(pkg, isAI, matchPercentage) {
    const sourceText = isAI ? 'AI Model' : 'Survey Analysis';
    const sourceIcon = isAI ? 'fa-brain' : 'fa-user-poll';
    const sourceClass = isAI ? 'ai-card' : 'survey-card';
    const labelClass = isAI ? 'ai-label' : 'survey-label';

    return `
    <div class="package-card ${sourceClass}">
            <div class="recommendation-label ${labelClass}">
                
                ${sourceText}
            </div>
            <div class="match-score">
                <i class="fa-solid fa-percentage"></i>
                Match: ${matchPercentage}%
            </div>
            ${pkg.source ? `<div class="recommendation-source">
                <i class="fa-solid fa-info-circle"></i>
                ${pkg.source}
            </div>` : ''}
        <div class="package-name">${pkg.name}</div>
        <div class="package-details">${pkg.kuota}</div>
        <div class="package-category">${pkg.category.charAt(0).toUpperCase() + pkg.category.slice(1)}</div>
        <div class="package-price">Rp ${pkg.harga.toLocaleString('id-ID')}</div>
        <button class="btn-choose ${isAI ? 'ai-choose' : 'survey-choose'}">
            <i class="fa-solid fa-check"></i>
            Pilih Paket
        </button>
    </div>`;
}

function showRecommendations() {
    recommendationsContainer.classList.add('active');
    surveyBtn.textContent = 'Retake Survey';
}

// Authentication is now handled by auth.js - these functions are removed

// Survey integration with AI Model + Survey Analysis
async function sendSurveyToPython(surveyData) {
    // Store locally for backup
    localStorage.setItem('surveyData', JSON.stringify(surveyData));

    try {
        const response = await fetch('http://localhost:8000/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(surveyData)
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                console.log('Hybrid recommendations received:', result.metadata);
                return result;
            }
        } else {
            throw new Error('Server error');
        }
    } catch (error) {
        console.log('AI Model server not available, using frontend calculation');
        return null; // Fallback to frontend calculation
    }

    return null;
}

// User profile is now handled by profile.html page

// Event Listeners for Authentication - these are now handled by auth.js
// The logout and profile functions are called directly from HTML onclick handlers

// Submit survey to server for authenticated users
async function submitSurveyToServer(userId, surveyData, recommendations) {
    try {
        const response = await fetch('http://localhost:8000/api/survey/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                survey_data: surveyData,
                recommendations: recommendations,
                selected_package: null // Can be updated when user selects a package
            })
        });

        const result = await response.json();
        if (result.success) {
            console.log('Survey submitted successfully to server');
        } else {
            console.error('Failed to submit survey:', result.error);
        }
    } catch (error) {
        console.error('Error submitting survey to server:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Auth state is now handled by auth.js
    // Survey initialization happens above if elements exist
});