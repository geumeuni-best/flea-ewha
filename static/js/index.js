document.addEventListener("DOMContentLoaded", () => {
  const isLoggedInEl = document.getElementById("is_logged_in");
  const isLoggedIn = isLoggedInEl?.value === "true";

  const regItemLink = document.querySelector('.navbar__menu li a[href="/reg_items"]');

  const loginModal = document.getElementById("loginModal");
  const closeLoginModal = document.getElementById("closeLoginModal");
  const goLogin = document.getElementById("goLogin");

  function showLoginModal() {
    loginModal.classList.remove("hidden");
  }

  function hideLoginModal() {
    loginModal.classList.add("hidden");
  }

  closeLoginModal?.addEventListener("click", hideLoginModal);
  loginModal?.addEventListener("click", (e) => {
    if (e.target === loginModal) hideLoginModal();
  });
  goLogin?.addEventListener("click", () => {
    window.location.href = "/login";
  });

  regItemLink?.addEventListener("click", (e) => {
    if (!isLoggedIn) {
      e.preventDefault();
      showLoginModal();
    }
  });
});
