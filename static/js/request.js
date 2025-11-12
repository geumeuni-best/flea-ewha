document.addEventListener("DOMContentLoaded", () => {
  const registerBtn = document.querySelector(".register-btn");

  const modal = document.getElementById("modal");
  const modalText = document.getElementById("modal-text");
  const modalConfirm = document.getElementById("modal-confirm");
  const modalLogin = document.getElementById("modal-login");
  const isLoggedInEl = document.getElementById("is_logged_in");
  const isLoggedIn = isLoggedInEl?.value === "true";

  function showModal(message, showLoginButton = false) {
    modalText.textContent = message;

    if (showLoginButton) {
      modalLogin.classList.remove("hidden");
    } else {
      modalLogin.classList.add("hidden");
    }

    modal.classList.remove("hidden");
  }

  function hideModal() {
    modal.classList.add("hidden");
  }

  modalConfirm.addEventListener("click", hideModal);
  modalLogin.addEventListener("click", () => {
    window.location.href = "/login";
  });
  modal.addEventListener("click", (e) => {
    if (e.target === modal) hideModal();
  });

  registerBtn?.addEventListener("click", (e) => {
    if (!isLoggedIn) {
      e.preventDefault();
      showModal("로그인이 필요합니다.", true);
      return;
    }

    window.location.href = "/reg_requests";
  });
});
