const closeBtn = document.querySelector("#fake_submit")
closeBtn.addEventListener("click", function() {
    setTimeout(() => {
        document.querySelector("#modal_submit_btn").click()
    }, 100)
})


const rateBtn = document.querySelectorAll(".rate_btn_song")
const modalWindow = document.querySelector("#openModal")

for (const btn of rateBtn) {
    btn.addEventListener("click", function() {
        const parent = this.parentElement
        const [nameEl, performerEl] = parent.querySelectorAll('input[type="hidden"]')
        modalWindow.querySelector(".modal-title").innerText = `${performerEl.value} - ${nameEl.value}`
        modalWindow.querySelector("#item_id").setAttribute("value", this.id)
        modalWindow.querySelector("#item_id").setAttribute("name", "song_id")
    })
}


const rateBtnAlbum = document.querySelectorAll(".rate_btn_album")

for (const btn of rateBtnAlbum) {
    btn.addEventListener("click", function() {
        const parent = this.parentElement
        const [nameEl, performerEl] = parent.querySelectorAll('input[type="hidden"]')
        modalWindow.querySelector(".modal-title").innerText = `${performerEl.value} - ${nameEl.value}`
        modalWindow.querySelector("#item_id").setAttribute("value", this.id)
        modalWindow.querySelector("#item_id").setAttribute("name", "album_id")
    })
}
