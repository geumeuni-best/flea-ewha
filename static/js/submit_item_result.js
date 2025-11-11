document.addEventListener("DOMContentLoaded", () => {
  // 수량
  const minusBtn = document.querySelector(".minus");
  const plusBtn = document.querySelector(".plus");
  const quantityEl = document.querySelector(".quantity");
  const totalAmountEl = document.querySelector(".amount");
  const tsumEl = document.querySelector(".tsum");

  // 상품 정보
  const priceText = totalAmountEl.textContent;
  const unitPrice = Number(priceText.replace(/[^0-9]/g, ""));
  const itemName = document.querySelector("h1").innerText;

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

  // 장바구니 버튼
  cartBtn.addEventListener("click", () => {
    showModal("🛒 장바구니에 추가되었습니다.");
  });

  // 구매 버튼
  buyBtn.addEventListener("click", async () => {
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
        modalClose.onclick = () => {
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
