const albums_select = document.querySelector("#album_id")
const perf_select = document.querySelector("#perf_id")
const songs_select = document.querySelector("#song_id")

async function set_options_songs(album_id){
    const response = await fetch(`/admin_songs?album_id=${album_id}`)
    const json_response = await response.json()
    const songs = json_response.songs
    if (!songs){
        return
    }
    songs_select.innerHTML = ""
    for (const song of songs){
        const option = document.createElement("option")
        option.innerHTML = song.song_name
        option.value = song.song_id
        songs_select.appendChild(option)
    }
}

async function set_options_albums(perf_id){
    const response = await fetch(`/admin_albums?perf_id=${perf_id}`)
    const json_response = await response.json()
    const albums = json_response.albums
    if (!albums){
        return
    }
    albums_select.innerHTML = ""
    for (const album of albums){
        const option = document.createElement("option")
        option.innerHTML = album.album_name
        option.value = album.album_id
        albums_select.appendChild(option)
    }
    set_options_songs(albums[0].album_id)
}

perf_select.addEventListener("change", function(){
    set_options_albums(this.value)
})

albums_select.addEventListener("change", function(){
    set_options_songs(this.value)
})

set_options_albums(perf_select.value)