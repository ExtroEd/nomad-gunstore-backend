document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('age-verification-overlay');
    const yesBtn = document.getElementById('yes-button');
    const noBtn = document.getElementById('no-button');
    const checkbox = document.getElementById('remember-check');

    // Проверка, сохранять ли
    if (sessionStorage.getItem('ageVerified') === 'true') {
      overlay.style.display = 'none';
    }

    yesBtn.addEventListener('click', () => {
      if (checkbox.checked) {
        sessionStorage.setItem('ageVerified', 'true');
      }
      overlay.style.display = 'none';
    });

    noBtn.addEventListener('click', () => {
      window.location.href = 'https://google.com'; // Куда отправить несовершеннолетних
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.querySelector('.header-button'); // или добавь отдельный id
    const modal = document.getElementById('login-modal');
    const closeBtn = document.getElementById('close-login-modal');

    loginBtn.addEventListener('click', (e) => {
      e.preventDefault(); // отключает переход
      modal.style.display = 'flex';
    });

    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
      if (e.target === modal) modal.style.display = 'none';
    });
});