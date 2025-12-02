document.addEventListener("DOMContentLoaded", () => {
  const btnCheck = document.getElementById("btn-check-username");
  const inputUsername = document.getElementById("username");

  btnCheck.addEventListener("click", async () => {
    const username = inputUsername.value.trim();

    if (!username) {
      alert("아이디를 입력해주세요!");
      inputUsername.focus();
      return;
    }

    try {
      const response = await fetch("/check_username", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username: username })
      });

      const data = await response.json();
      alert(data.msg);

      // 사용 가능하면 border 색상 초록색
      if (data.ok) {
        inputUsername.style.border = "2px solid #28a745";
      } else {
        inputUsername.style.border = "2px solid #dc3545";
      }

    } catch (error) {
      console.error("중복확인 오류:", error);
      alert("서버와 통신 중 오류가 발생했습니다.");
    }
  });
});
