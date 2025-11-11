document.addEventListener("DOMContentLoaded", function () {
  let items = [];
  let selectedItem = null;

  fetch("/api/items")
    .then(response => response.json())
    .then(data => {
      items = data.items || [];
    });

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

  function updateSelectedItem(item) {
    document.querySelector(".product-name").textContent = item.name;
    document.querySelector(".product-img").src = "/static/image/" + item.img_path;
    document.querySelector(".product-seller").textContent = "품절";
    document.getElementById("selected_item_img").value = item.img_path.startsWith("image/")
      ? item.img_path
      : "image/" + item.img_path;
  }
});

function updateSelectedItem(item) {
  document.querySelector(".product-name").textContent = item.name;
  document.querySelector(".product-img").src = "/static/image/" + item.img_path;
  document.querySelector(".product-seller").textContent = "품절";

  document.querySelector(".stars").textContent = "★".repeat(item.stars || 0) + "☆".repeat(5 - (item.stars || 0));
  document.querySelector(".rating-value").textContent = "(" + (item.rating_count || 0) + ")";

  document.getElementById("selected_item").value = item.name;
  document.getElementById("selected_item_img").value = item.img_path;
}

function onSelectItem(itemName, itemData) {
  document.querySelector('.product-name').textContent = itemName;
  document.querySelector('.product-seller').textContent = itemData.status || '품절';
  if (itemData.img_path) {
    document.getElementById('product-img').src = `/static/image/${itemData.img_path}`;
  }

  document.getElementById('selected_item').value = itemName;
}