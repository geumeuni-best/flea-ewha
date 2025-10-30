function updateFileName(input) {
  const fileName = input.files.length > 0 ? input.files[0].name : "선택된 파일 없음";
  document.getElementById("file-name").textContent = fileName;
}