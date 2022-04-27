const searchForm = document.querySelector("#user_form")

function searchHtml(r){
    return `
        <div>
            <li>
                <h4>${r.title}</h4>
                <a href="/details/${r.id}">             
                    <img src="${r.image}" alt="${r.title}">
                </a>
            </li>
    `;
}

searchForm.addEventListener("submit", function(e){
    e.preventDefault();
    const search_q = document.getElementById('Ingredient')
    console.log(search_q.value)
    getResults(search_q.value)
});

async function getResults(q) {
    
    const response = await axios.get("https://api.spoonacular.com/recipes/findByIngredients", {params: {'apiKey': 'e3e74bc5b1e646ae8888b3f7dca142f6','ingredients': q, 'number': '2'}});

    for (let r of response.data) {
        let lineItem = $(searchHtml(r));
        $("#search-results").append(lineItem)
        console.log(r['[title]'])
    }

    console.log(response.data)


}

