
const searchEndpoint = "http://localhost:6969/search";

input.addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        search();
    }
});

async function search(){

    const container = document.getElementById("results");
    container.innerHTML = "<div class='loading'>Searching...</div>";

    const query = document.getElementById("queryInput").value;
    const topN = parseInt(document.getElementById("topNInput").value) || 5;

    try {

        const response = await fetch(searchEndpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query,
                top_k: topN
            })
        });

        const data = await response.json();

        renderResults(data.results);

    } catch (err) {

        container.innerHTML =
            "<div class='loading'>Error connecting to server</div>";

        console.error(err);
    }
}

function renderResults(results){

    const container = document.getElementById("results");
    container.innerHTML = "";

    if(!results || results.length === 0){
        container.innerHTML = "<div class='loading'>No results found</div>";
        return;
    }

    results.forEach((article,index)=>{

        const card = document.createElement("div");
        card.className = "card";
        card.style.animationDelay = `${index*0.07}s`;

        const shortText = article.text.substring(0,120);

        card.innerHTML = `
        <h3>${article.title}</h3>
        <p class="text">${shortText}...</p>
        <div class="expand">Show more</div>
        <div class="score">Similarity score: ${article.score.toFixed(3)}</div>
        `;

        const text = card.querySelector(".text");
        const expand = card.querySelector(".expand");

        expand.onclick = () => {

            if(expand.innerText === "Show more"){
                text.innerText = article.text;
                expand.innerText = "Show less";
            } else {
                text.innerText = shortText + "...";
                expand.innerText = "Show more";
            }

        };

        container.appendChild(card);

    });
}