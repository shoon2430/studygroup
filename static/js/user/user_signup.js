const hint_question = document.getElementById("id_hint_question");
const hint = document.getElementById("id_hint");

hint_question.addEventListener("change", () => {
  hint.value = "";
});
