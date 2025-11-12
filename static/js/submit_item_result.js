document.addEventListener("DOMContentLoaded", () => {
  const minusBtn = document.querySelector(".minus");
  const plusBtn = document.querySelector(".plus");
  const quantityEl = document.querySelector(".quantity");
  const totalAmountEl = document.querySelector(".amount");
  const tsumEl = document.querySelector(".tsum");
  const cartBtn = document.querySelector(".cart");
  const buyBtn = document.querySelector(".buy");

  const modal = document.getElementById("modal");
  const modalText = document.getElementById("modal-text");
  const modalConfirm = document.getElementById("modal-confirm");
  const modalLogin = document.getElementById("modal-login");

  const isSoldoutEl = document.getElementById("is_soldout");
  const isSoldout = isSoldoutEl?.value === "true";

  const isLoggedInEl = document.getElementById("is_logged_in");
  const isLoggedIn = isLoggedInEl?.value === "true";

  const itemName = document.querySelector("h1")?.innerText || "";
  const priceText = totalAmountEl?.textContent || "0";
  const unitPrice = Number(priceText.replace(/[^0-9]/g, ""));
  let quantity = 1;

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

  function updateAmount() {
    const totalPrice = unitPrice * quantity;
    quantityEl.textContent = quantity;
    tsumEl.textContent = `총 수량 ${quantity}개 `;
    totalAmountEl.textContent = `${totalPrice.toLocaleString()}원`;
  }

  updateAmount();

  if (isSoldout) {
    [minusBtn, plusBtn].forEach((btn) => btn && (btn.disabled = true));
    quantityEl.textContent = "0";
    tsumEl.textContent = "품절된 상품입니다";
    totalAmountEl.textContent = "-";

    [cartBtn, buyBtn].forEach((btn) => {
      btn?.addEventListener("click", (e) => {
        e.preventDefault();
        showModal("❌ 품절된 상품은 구매할 수 없습니다.");
      });
    });

    return;
  }

  minusBtn?.addEventListener("click", () => {
    if (quantity > 1) {
      quantity--;
      updateAmount();
    }
  });

  plusBtn?.addEventListener("click", () => {
    quantity++;
    updateAmount();
  });

  cartBtn?.addEventListener("click", () => {
    if (!isLoggedIn) {
      showModal("로그인이 필요합니다.", true);
      return;
    }
    showModal("🛒 장바구니에 추가되었습니다.");
  });

  buyBtn?.addEventListener("click", async () => {
    if (!isLoggedIn) {
      showModal("로그인이 필요합니다.", true);
      return;
    }

    const formData = new FormData();
    formData.append("item_name", itemName);
    formData.append("quantity", quantity);

    try {
      const response = await fetch("/buy_item", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        showModal(`💳 ${result.message || "구매가 완료되었습니다."}`);
        modalConfirm.onclick = () => {
          hideModal();
          window.location.href = "/mypage";
        };
      } else {
        showModal(result.error || "구매 중 오류가 발생했습니다.");
      }
    } catch (error) {
      console.error(error);
      showModal("서버 연결에 실패했습니다.");
    }
  });
});
