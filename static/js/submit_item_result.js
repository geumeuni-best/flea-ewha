document.addEventListener("DOMContentLoaded", () => {
  // 수량
  const minusBtn = document.querySelector(".minus");
  const plusBtn = document.querySelector(".plus");
  const quantityEl = document.querySelector(".quantity");
  const totalAmountEl = document.querySelector(".amount");
  const tsumEl = document.querySelector(".tsum");

  const priceText = totalAmountEl.textContent;
  const unitPrice = Number(priceText.replace(/[^0-9]/g, ""));
  let quantity = 1;

  function updateAmount() {
    const totalPrice = unitPrice * quantity;
    quantityEl.textContent = quantity;
    tsumEl.textContent = `총 수량 ${quantity}개 `;
    totalAmountEl.textContent = `${totalPrice.toLocaleString()}원`;
  }

  minusBtn.addEventListener("click", () => {
    if (quantity > 1) {
      quantity--;
      updateAmount();
    }
  });

  plusBtn.addEventListener("click", () => {
    quantity++;
    updateAmount();
  });

  updateAmount();

  // 모달
  const modal = document.getElementById("modal");
  const modalText = document.getElementById("modal-text");
  const modalClose = document.getElementById("modal-close");

  function showModal(message) {
    modalText.textContent = message;
    modal.classList.remove("hidden");
  }

  function hideModal() {
    modal.classList.add("hidden");
  }

  modalClose.addEventListener("click", hideModal);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) hideModal();
  });

  // 버튼 
  const cartBtn = document.querySelector(".cart");
  const buyBtn = document.querySelector(".buy");

  cartBtn.addEventListener("click", () => {
    showModal("🛒 장바구니에 추가되었습니다.");
  });

  buyBtn.addEventListener("click", () => {
    showModal("💳 구매가 완료되었습니다.");
  });
});
