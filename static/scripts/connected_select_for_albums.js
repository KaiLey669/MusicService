const albums_select2 = document.querySelector("#album2_id")
const perf_select2 = document.querySelector("#perf2_id")

console.log('lol')

async function set_options_albums2(perf_id){
    const response = await fetch(`/admin_albums2?perf_id=${perf_id}`)
    const json_response = await response.json()
    const albums = json_response.albums
    if (!albums){
        return
    }
    albums_select2.innerHTML = ""
    for (const album of albums){
        const option = document.createElement("option")
        option.innerHTML = album.album_name
        option.value = album.album_id
        albums_select2.appendChild(option)
    }
}

perf_select2.addEventListener("change", function(){
    set_options_albums2(this.value)
})

set_options_albums2(perf_select2.value)