function leaderboards(){
    let data = {};

    
    for(let i = 0; i < 100; i++){
        data[`bot${i}`] = i * 100
    }
    
    data = merge_sort(data);

    let html = ``;
    let place = 1;
    for (const key in data){
        html += 
        `<div class="player-result" data-place="${place > 50 ? "50+": place}">
           <div class="place">#${place}</div>
           <div class="nickname">${key}</div>
           <div class="score">${data[key]}</div>
        </div>\n`;

        place += 1;
    }

    document.getElementById("leaderboard").innerHTML = html;
}

function merge_sort(data) {
    let player_data = [];

    for (const key in data) {
        player_data.push({[key]: data[key] });
    }

    for (let width = 1; width < player_data.length; width *= 2) {
        let merged = [];

        for (let i = 0; i < player_data.length; i += width * 2) {
            let left = player_data.slice(i, i + width);
            let right = player_data.slice(i + width, i + width * 2);

            let l = 0;
            let r = 0;

            while (l < left.length && r < right.length) {
                let leftValue = Object.values(left[l])[0];
                let rightValue = Object.values(right[r])[0];

                if (leftValue >= rightValue) {
                    merged.push(left[l++]);
                } else {
                    merged.push(right[r++]);
                }
            }

            while (l < left.length) {
                merged.push(left[l++]);
            }

            while (r < right.length) {
                merged.push(right[r++]);
            }
        }

        player_data = merged;
    }

    data = {};
    for(let index = 0; index < player_data.length - 1; index++){
        data[Object.keys(player_data[index])] = 
        player_data[index][Object.keys(player_data[index])[0]]
    }

    return data;
}

