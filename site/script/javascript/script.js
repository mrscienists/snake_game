async function leaderboards(){
    const data = await get_score();

    let html = ``;
    place = 1;
    for(let player in data){
        html += 
        `<div class="player-result" data-place="${place > 50 ? "50+": place}">
           <div class="place">#${place}</div>
           <div class="nickname">${data[player]["player"]}</div>
           <div class="score">${data[player]["score"]}</div>
        </div>\n`;

        place += 1;
    }

    document.getElementById("leaderboard").innerHTML = html;
}

async function get_score(){
    try {
        const response = await fetch("http://localhost:8000/score");

        if(!response.ok){
            throw new Error(`Error in HTTP: ${response.status}`);
        }
        const data = await response.json();

        return data;
    } catch (error){
        console.error("Error in request:", error)
    }
}