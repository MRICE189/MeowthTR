var allPokemon = []

function getPokemon(id) {
    fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
    .then(resp => resp.json())
    .then(data => {
        let gen = data.game_indices[0].version.name
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
        allPokemon.push(pokemon_data)
    })
    .catch(err => console.log(err))
}

for (i=1; i<=649; i++) {
    getPokemon(i)
}
console.log(allPokemon)

var fillDbBtn = document.querySelector('#fill-db-btn')

fillDbBtn.addEventListener('click', function() {
    fetch ('/fill_db', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(allPokemon)
        })
    .then(resp => {
        if (resp.ok) {
            return resp.json()}
        else {
            alert('something went wrong')
        }})
    .then(data => {
        for (pokemon in data) {
            console.log(pokemon)
        }
    })
    .catch(err => {
        console.log(err)
    })
})