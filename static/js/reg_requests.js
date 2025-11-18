document.addEventListener("DOMContentLoaded", function () {
  let items = [];
  let selectedItem = null;

  // 상품 데이터 가져오기
  fetch("/api/items")
    .then(response => response.json())
    .then(data => {
      items = data.items || [];
    });

  // 검색 기능
  document.getElementById("search").addEventListener("input", function (e) {
    const keyword = e.target.value.trim();
    const listDiv = document.getElementById("item-search-result");
    listDiv.innerHTML = "";
    if (keyword.length === 0) return;

    const results = items.filter(item => item.name.includes(keyword));
    results.forEach(item => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "search-result-btn";
      btn.textContent = item.name;
      btn.onclick = function () {
        selectedItem = item;
        updateSelectedItem(item);
        document.getElementById("search").value = item.name;
        listDiv.innerHTML = "";
      };
      listDiv.appendChild(btn);
    });
  });

});

// 선택된 상품 정보 업데이트
function updateSelectedItem(item) {
  document.querySelector(".product-name").textContent = item.name;
  document.querySelector(".product-img").src = "/static/image/" + item.img_path;
  document.querySelector(".product-seller").textContent = "품절";

  const stars = item.stars || 0;
  document.querySelector(".stars").textContent =
    "★".repeat(stars) + "☆".repeat(5 - stars);

  document.querySelector(".rating-value").textContent =
    "(" + (item.rating_count || 0) + ")";

  document.getElementById("selected_item").value = item.name;
  document.getElementById("selected_item_img").value = item.img_path;
}
