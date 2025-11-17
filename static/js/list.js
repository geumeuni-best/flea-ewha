function toggleLike(itemName) {
  event.stopPropagation();

  const isLoggedIn = document.getElementById("is_logged_in").value === "true";

  if (!isLoggedIn) {
    document.getElementById("loginModal").classList.remove("hidden");
    return;
  }

  const heart = event.currentTarget.querySelector(".heart-icon");
  const liked = heart.classList.contains("liked");

  heart.classList.toggle("liked");

  const url = liked ? `/unlike/${itemName}/` : `/like/${itemName}/`;
  const data = liked ? { interested: "N" } : { interested: "Y" };

  $.ajax({
    type: "POST",
    url: url,
    data: data,
    success: function (response) {
      alert(response.msg);
    },
    error: function () {
      alert("오류가 발생했습니다.");
      heart.classList.toggle("liked");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("loginModal");
  const closeBtn = document.getElementById("closeLoginModal");
  const goLogin = document.getElementById("goLogin");

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  if (goLogin) {
    goLogin.addEventListener("click", () => {
      window.location.href = "/login";
    });
  }
});
