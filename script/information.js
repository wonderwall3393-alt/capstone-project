document.addEventListener("DOMContentLoaded", function () {
  initPaymentSteps();
  initFAQ();
  initContactForm();
  initSmoothScroll();
});

// PAYMENT STEPS
function initPaymentSteps() {
  const steps = document.querySelectorAll(".step");
  const contentBoxes = document.querySelectorAll(".content-box");

  steps.forEach((step) => {
    step.addEventListener("click", function () {
      const stepNumber = this.getAttribute("data-step");

      steps.forEach((s) => {
        s.classList.remove("active");
        s.style.transform = "scale(1)";
      });

      this.classList.add("active");
      this.style.transform = "scale(1.02)";

      contentBoxes.forEach((box) => {
        box.style.opacity = "0";
        box.style.transform = "translateX(20px)";
        setTimeout(() => {
          box.classList.remove("active");
        }, 150);
      });

      setTimeout(() => {
        const targetContent = document.querySelector(
          `[data-content="${stepNumber}"]`
        );
        if (targetContent) {
          targetContent.classList.add("active");
          setTimeout(() => {
            targetContent.style.opacity = "1";
            targetContent.style.transform = "translateX(0)";
          }, 50);
        }
      }, 150);
    });
  });

  const firstContent = document.querySelector('[data-content="1"]');
  if (firstContent) {
    firstContent.style.opacity = "1";
    firstContent.style.transform = "translateX(0)";
  }
}

// FAQ
function initFAQ() {
  const faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");
    answer.style.maxHeight = "0px";
    answer.style.overflow = "hidden";

    question.addEventListener("click", function () {
      const isActive = item.classList.contains("active");
      faqItems.forEach((faq) => {
        faq.classList.remove("active");
        const ans = faq.querySelector(".faq-answer");
        ans.style.maxHeight = "0px";
        ans.style.padding = "0 30px";
      });

      if (!isActive) {
        item.classList.add("active");
        answer.style.maxHeight = answer.scrollHeight + 50 + "px";
        answer.style.padding = "25px 30px";
      }
    });
  });
}

// CONTACT FORM
function initContactForm() {
  const contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const submitBtn = contactForm.querySelector(".btn-submit");
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML =
        '<i class="fa-solid fa-spinner fa-spin"></i> Mengirim...';
      submitBtn.disabled = true;

      setTimeout(() => {
        showSuccessMessage();
        contactForm.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }, 1500);
    });
  }
}

function showSuccessMessage() {
  const messageDiv = document.createElement("div");
  messageDiv.className = "success-message";
  messageDiv.innerHTML = `<i class="fa-solid fa-check-circle"></i> <span>Pesan Anda telah terkirim!</span>`;

  messageDiv.style.cssText = `
        position: fixed; top: 100px; right: 20px; background: #4CAF50; color: white;
        padding: 20px 30px; border-radius: 10px; box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        display: flex; align-items: center; gap: 15px; z-index: 10000;
        animation: slideInRight 0.4s ease, slideOutRight 0.4s ease 3s forwards;
        font-family: inter; font-weight: 500;
    `;
  document.body.appendChild(messageDiv);
  setTimeout(() => messageDiv.remove(), 3500);
}

// SMOOTH SCROLL
function initSmoothScroll() {
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (href === "#" || href === "#top") {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
        return;
      }
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        const headerHeight = document.querySelector("header").offsetHeight;
        const targetPosition = target.offsetTop - headerHeight - 30;
        window.scrollTo({ top: targetPosition, behavior: "smooth" });
      }
    });
  });
}

// ADD ANIMATION STYLE
const style = document.createElement("style");
style.textContent = `
    @keyframes slideInRight { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes slideOutRight { from { transform: translateX(0); opacity: 1; } to { transform: translateX(400px); opacity: 0; } }
`;
document.head.appendChild(style);
