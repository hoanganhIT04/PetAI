let DATA = null;
const modal = new bootstrap.Modal(document.getElementById("detailModal"));

/* ================= FETCH DATA ================= */
fetch("http://127.0.0.1:8000/data-progress")
  .then(res => res.json())
  .then(data => {
    console.log("DATA:", data);
    DATA = data;
    renderMain();
  })
  .catch(err => console.error(err));


/* ================= UTILS ================= */
function percent(cur, target) {
  return ((cur / target) * 100).toFixed(1);
}

function percentCapped(cur, target) {
  return Math.min((cur / target) * 100, 100).toFixed(1);
}


function setBar(id, cur, target) {
  const realPercent = Number(percent(cur, target));
  const cappedPercent = Math.min(realPercent, 100);

  document.getElementById(`${id}-text`).innerText =
    `${cur} / ${target} (${realPercent}%)`;

  const bar = document.getElementById(`${id}-bar`);
  bar.style.width = cappedPercent + "%";
  bar.innerText = realPercent + "%";

  // reset màu
  bar.classList.remove("bg-danger", "bg-success", "bg-warning");

  if (realPercent < 40) {
    bar.classList.add("bg-danger");      // 🔴 thiếu
  } else if (realPercent <= 100) {
    bar.classList.add("bg-success");     // 🟢 đạt
  } else {
    bar.classList.add("bg-warning");     // 🟡 vượt
  }
}

/* ================= MAIN DASHBOARD ================= */
function renderMain() {
  if (!DATA) return;

  // Model 1
  setBar(
    "m1-animal",
    DATA.model_1.animal.current,
    DATA.model_1.animal.target
  );

  setBar(
    "m1-non",
    DATA.model_1.non_animal.current,
    DATA.model_1.non_animal.target
  );

  // Model 2
  setBar(
    "m2-breed",
    DATA.model_2.breed.current,
    DATA.model_2.breed.target
  );

  setBar(
    "m2-unknown",
    DATA.model_2.unknown.current,
    DATA.model_2.unknown.target
  );
}

/* ================= MODAL DETAIL ================= */
function openModal(type) {
  if (!DATA) return;

  const table = document.getElementById("modalTable");
  table.innerHTML = "";

  let title = "";
  let detail = [];

  if (type === "m1_animal") {
    title = "Model 1 – Animal Detail";
    detail = DATA.model_1.animal.detail;
  }

  if (type === "m1_non") {
    title = "Model 1 – Non-Animal Detail";
    detail = DATA.model_1.non_animal.detail;
  }

  if (type === "model2") {
    title = "Model 2 – Breed Detail";
    detail = DATA.model_2.breed.detail;
  }

  document.getElementById("modalTitle").innerText = title;

  detail.forEach((item, index) => {
    table.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${item.name || item.breed}</td>
        <td>${item.count}</td>
      </tr>
    `;
  });

  modal.show();
}
