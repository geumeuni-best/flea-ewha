function toggleLike(itemName) {
  const btn = event.currentTarget.querySelector(".heart-icon");
  const liked = btn.classList.toggle("liked");

  // 백엔드 연동 후 수정 예정
  // fetch(`/like/${itemName}`, {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ liked })
  // });
}