
apiKey = 'e3e74bc5b1e646ae8888b3f7dca142f6'
const searchForm = document.getElementById('search_form')


// Homepage search results
function searchHtml(r){
    return `
        <div class='card'>
            <a href="/details/${r.id}">             
                <h4>${r.title}</h4>
                <img src="${r.image}" alt="${r.title}">
            </a>
        </div>
    `;
}

searchForm.addEventListener("submit", function(e){
    e.preventDefault();
    const search_q = document.getElementById('Ingredient')

    getResults(search_q.value)
});

async function getResults(q) {
    
    const response = await axios.get("https://api.spoonacular.com/recipes/findByIngredients", {params: {'apiKey': apiKey,'ingredients': q, 'number': '6'}});

    for (let r of response.data) {
        let lineItem = $(searchHtml(r));
        $("#search-results").append(lineItem)
    }
}




