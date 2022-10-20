var guessBtn = document.querySelector('.guess')

function guess() {
    form = new FormData(guessBtn)
    fetch("/api/guess", {
        method: 'POST',
        body: form
    })
    .then(resp => resp.json())
    .then(data => {
        // console.log(data);
        if (data.msg) {
            console.log('not a valid Pokémon')
        }
        else {
        return getPokemon(data.pokemon_id)
        }
    })
    .catch(err => {
        console.log(err);
    })
}

async function getPokemon(id) {
    pokemon = id;
    let resp = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`)
    data = await resp.json()
    let pokemon_data = {
        'poke_name': data.forms[0].name,
        'poke_height': data.height,
        'poke_sprite': data.sprites.front_default,
        'poke_type1': data.types[0].type.name,
        'poke_weight': data.weight,
        'poke_id': data.id,
        'poke_att': data.stats[1].base_stat,
        'poke_satt': data.stats[3].base_stat,
    }
    let gen = data.game_indices[0].version.name
        if (data.types[1] != undefined) {
            pokemon_data['poke_type2'] = data.types[1].type.name
        }
        else {
            pokemon_data['poke_type2'] = 'none'
        }
    if (gen == 'red' || gen == 'blue') {pokemon_data['poke_gen'] = 1}
    else if (gen == 'silver' || gen == 'gold') {pokemon_data['poke_gen'] = 2}
    else if (gen == 'ruby' || gen == 'sapphire') {pokemon_data['poke_gen'] = 3}
    else if (gen == 'diamond' || gen == 'pearl') {pokemon_data['poke_gen'] = 4}
    else if (gen == 'black' || gen == 'white') {pokemon_data['poke_gen'] = 5}
    else {console.log('unknown gen')}
    form = new FormData()
    for (const item in pokemon_data) {
        form.append(item, pokemon_data[item])
    }
    let resp2 = await fetch('/api/compare', {
        method: 'POST',
        body: form
    })
    data2 = await resp2.json()
    drawElements(pokemon_data, data2);
    check_win(pokemon_data, data2);
}

async function check_win(data, data2) {
    let drawDiv = document.querySelector('#results')
    let drawEl = document.createElement('h1')
    let removeGuess = document.querySelector('.guess')
    let playBtn = document.querySelector('#play_again')
    if (data2.comp_name == 'match') {
        //win condition
        let resp = await fetch('/api/win', {
            method: 'POST'
        })
        drawEl.textContent = 'You Win!'
        drawEl.classList.add('text-white')
        drawDiv.classList.remove('d-none')
        drawDiv.classList.add('bg-success')
        removeGuess.remove();
        playBtn.classList.remove('d-none')
    }
    else if (data2.guess_num === 8) {
        //lose condition
        let resp = await fetch('/api/lose', {
            method: 'POST'
        })
        let name = data2.target_name
        name = name.charAt(0).toUpperCase() + name.slice(1);
        drawEl.textContent = `You lose, sorry! It was ${name}`
        drawEl.classList.add('text-white')
        drawDiv.classList.remove('d-none')
        drawDiv.classList.add('bg-danger')
        removeGuess.remove();
        playBtn.classList.remove('d-none')
    }
    drawDiv.appendChild(drawEl)
}

function drawElements(data, data2) {
    drawName(data, data2);
    drawSprite(data, data2);
    drawGen(data, data2);
    drawType1(data, data2);
    drawType2(data, data2);
    drawAtt(data, data2);
    drawSatt(data, data2);
    drawHeight(data, data2);
    drawWeight(data, data2)
}

function drawName(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let name = data.poke_name
    name = name.charAt(0).toUpperCase() + name.slice(1);
    let drawEl = document.createElement('td')
    if (data2.comp_name == 'match') {
        drawEl.textContent = name
        drawEl.classList.add('text-success')
    } else {
        drawEl.textContent = name
        drawEl.classList.add('text-danger')
    }
    drawDiv.appendChild(drawEl)
}

function drawSprite(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let sprite = data.poke_sprite;
    let drawEl = document.createElement('td');
    let innerEl = document.createElement('img')
    innerEl.src = sprite
    innerEl.classList.add('sprite');
    drawEl.appendChild(innerEl)
    drawDiv.appendChild(drawEl)
}

function drawGen(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let drawEl = document.createElement('td');
    let innerEl = document.createElement('img')
    innerEl.classList.add('icon');
    if (data2.comp_gen == 'match') {
        innerEl.src = "../static/img/check.png"
    } else if (data2.comp_gen == '^') {
        innerEl.src = "../static/img/up.png"
    } else {
        innerEl.src = "../static/img/down.png"
    }
    drawEl.appendChild(innerEl)
    drawDiv.appendChild(drawEl)
}

function drawType1(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let type1 = data.poke_type1
    type1 = type1.charAt(0).toUpperCase() + type1.slice(1);
    let drawEl = document.createElement('td')
    if (data2.comp_type1 == 'match') {
        drawEl.textContent = type1
        drawEl.classList.add('text-success')
    } else {
        drawEl.textContent = type1
        drawEl.classList.add('text-danger')
    }
    drawDiv.appendChild(drawEl)
}

function drawType2(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let type2 = data.poke_type2
    type2 = type2.charAt(0).toUpperCase() + type2.slice(1);
    let drawEl = document.createElement('td')
    if (data2.comp_type2 == 'match') {
        drawEl.textContent = type2
        drawEl.classList.add('text-success')
    } else {
        drawEl.textContent = type2
        drawEl.classList.add('text-danger')
    }
    drawDiv.appendChild(drawEl)
}

function drawAtt(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let drawEl = document.createElement('td');
    let innerEl = document.createElement('img')
    innerEl.classList.add('icon');
    if (data2.comp_att == 'match') {
        innerEl.src = "../static/img/check.png"
    } else if (data2.comp_att == '^') {
        innerEl.src = "../static/img/up.png"
    } else {
        innerEl.src = "../static/img/down.png"
    }
    drawEl.appendChild(innerEl)
    drawDiv.appendChild(drawEl)
}

function drawSatt(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let drawEl = document.createElement('td');
    let innerEl = document.createElement('img')
    innerEl.classList.add('icon');
    if (data2.comp_satt == 'match') {
        innerEl.src = "../static/img/check.png"
    } else if (data2.comp_satt == '^') {
        innerEl.src = "../static/img/up.png"
    } else {
        innerEl.src = "../static/img/down.png"
    }
    drawEl.appendChild(innerEl)
    drawDiv.appendChild(drawEl)
}

function drawHeight(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let drawEl = document.createElement('td');
    let innerEl = document.createElement('img')
    innerEl.classList.add('icon');
    if (data2.comp_height == 'match') {
        innerEl.src = "../static/img/check.png"
    } else if (data2.comp_height == '^') {
        innerEl.src = "../static/img/up.png"
    } else {
        innerEl.src = "../static/img/down.png"
    }
    drawEl.appendChild(innerEl)
    drawDiv.appendChild(drawEl)
}

function drawWeight(data, data2) {
    let drawDiv = document.querySelector(`#guess${data2.guess_num}`)
    let drawEl = document.createElement('td');
    let innerEl = document.createElement('img')
    innerEl.classList.add('icon');
    if (data2.comp_weight == 'match') {
        innerEl.src = "../static/img/check.png"
    } else if (data2.comp_weight == '^') {
        innerEl.src = "../static/img/up.png"
    } else {
        innerEl.src = "../static/img/down.png"
    }
    drawEl.appendChild(innerEl)
    drawDiv.appendChild(drawEl)
}

searchBar = document.querySelector('#search-bar')

guessBtn.addEventListener('submit', function(event) {
    event.preventDefault();
    console.log('guess submitted')
    guess()
    searchBar.value = "";
    window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);
})

//search auto-complete elements
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box")

inputBox.onkeyup = (event)=>{
    let userData = event.target.value; //user entered data
    let emptyArray = [];
    if (userData) {
        emptyArray = suggestions.filter((data)=> {
            //filtering array value
            return data.toLowerCase().startsWith(userData.toLowerCase());
        });
        emptyArray = emptyArray.map((data)=> {
            data = data.charAt(0).toUpperCase() + data.slice(1);
            return data = '<li>' + data + '</li>';
        })
        console.log(emptyArray)
        searchWrapper.classList.add('active'); //show suggestions
        showSuggestions(emptyArray);
        let allList = suggBox.querySelectorAll('li');
        for (let i = 0; i < allList.length; i++) {
            allList[i].setAttribute("onclick", "select(this)");
        }
    }
    else {
        searchWrapper.classList.remove('active'); //hide suggestions when empty
        showSuggestions(emptyArray);
    }
}

function select(element) {
    let selectUserData = element.textContent;
    inputBox.value = selectUserData; //passes the selected mon into the search box when clicked
    suggBox.innerHTML = "";
    searchWrapper.classList.remove('active')
}

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        listData = []
    } else {
        listData = list.join(' ');
    }
    suggBox.innerHTML = listData;
}