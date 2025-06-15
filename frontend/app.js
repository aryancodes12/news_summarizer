const container = document.getElementById("news-container");
const loading = document.getElementById("loading");
const API_URL = "http://localhost:8000/news";

// Load news from backend and populate cards
async function loadNews() {
  loading.style.display = "block";
  container.innerHTML = "";

  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    data.forEach(article => {
      const card = document.createElement("div");
      card.className = "article";

      card.innerHTML = `
    <span class="category">${article.category || "General"}</span>
    <img src="${article.thumbnail || 'https://via.placeholder.com/350x180'}" alt="Unable to load image. Sorry for inconvenience.">
    <h2>${article.title}</h2>
    <p>${article.summary}</p>
    <a href="${article.url}" target="_blank">Read more ➜</a>
`;

      container.appendChild(card);
    });
  } catch (error) {
    console.error("Error loading news:", error);
    container.innerHTML = `<p style="text-align:center; color:red;">Failed to load news. Please try again later.</p>`;
  }

  loading.style.display = "none";
}

// Initial load and auto-refresh every 3 minutes
loadNews();
setInterval(loadNews, 120000);