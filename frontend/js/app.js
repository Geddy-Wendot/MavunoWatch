const allCrops = [];
let chartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  const isTrendPage = document.getElementById("trendForm") !== null;
  const isPredictPage = document.getElementById("predict-form") !== null;

  if (isTrendPage) setupTrendPage();
  if (isPredictPage) setupPredictPage();
});

// 🔧 Setup for Prediction Page (index.html)
function setupPredictPage() {
  const predictCounty = document.getElementById("predict-county");
  const predictCrop = document.getElementById("predict-crop");
  const areaInput = document.getElementById("area");
  const predictForm = document.getElementById("predict-form");
  const resultDiv = document.getElementById("prediction-result");

  fetch("http://127.0.0.1:5000/metadata")
    .then(res => res.json())
    .then(data => {
      data.counties.forEach(c => {
        predictCounty.innerHTML += `<option value="${c}">${c}</option>`;
      });
      data.crops.forEach(c => {
        predictCrop.innerHTML += `<option value="${c}">${c}</option>`;
        allCrops.push(c);
      });
    });

  predictForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const county = predictCounty.value;
    const crop = predictCrop.value;
    const area = parseFloat(areaInput.value);
    const year = new Date().getFullYear();

    const payload = {
      year,
      area_ha: area,
      crop,
      all_crops: allCrops
    };

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (data.predicted_yield) {
        resultDiv.innerHTML = `<h3>🌽 Predicted Yield: ${data.predicted_yield} tons/ha</h3>`;
      } else {
        resultDiv.innerHTML = `<p class="warning">⚠️ ${data.error}</p>`;
      }

    } catch (err) {
      resultDiv.innerHTML = `<p class="warning">🔥 Prediction failed: ${err.message}</p>`;
    }
  });
}

// 🔧 Setup for Trend Page (trends.html)
if (document.getElementById("trendForm")) {
  const trendCounty = document.getElementById("county");
  const trendCrop = document.getElementById("crop");
  const trendForm = document.getElementById("trendForm");
  const trendNote = document.getElementById("trendNote");
  const trendCanvas = document.getElementById("trendChart")?.getContext("2d");

  fetch("http://127.0.0.1:5000/metadata")
    .then(res => res.json())
    .then(data => {
      data.counties.forEach(c => {
        trendCounty.innerHTML += `<option value="${c}">${c}</option>`;
      });
      data.crops.forEach(c => {
        trendCrop.innerHTML += `<option value="${c}">${c}</option>`;
      });
    });

  trendForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const county = trendCounty.value;
    const crop = trendCrop.value;

    try {
      const res = await fetch("http://127.0.0.1:5000/trend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ county, crop })
      });

      const data = await res.json();

      if (data.error || !data.trend) {
        trendNote.innerHTML = `<p class="warning">${data.error || "No trend data."}</p>`;
        return;
      }

      const years = data.trend.map(t => t.year);
      const yields = data.trend.map(t => t.yield);

      if (chartInstance) chartInstance.destroy();

      chartInstance = new Chart(trendCanvas, {
        type: "line",
        data: {
          labels: years,
          datasets: [{
            label: `Yield Trend for ${crop} in ${county}`,
            data: yields,
            borderColor: "green",
            backgroundColor: "rgba(0,128,0,0.2)",
            borderWidth: 2,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: false
            }
          }
        }
      });

      trendNote.innerHTML = `<p class="info">${data.trend_note}</p>`;

    } catch (err) {
      trendNote.innerHTML = `<p class="warning">🔥 Trend fetch failed: ${err.message}</p>`;
    }
  });
}
