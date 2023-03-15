
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




// function popupOpenClose(popup) {

//     /* Add div inside popup for layout if one doesn't exist */
//     if ($(".wrapper", popup).length == 0) {
//         $(popup).wrapInner("<div class='wrapper'></div>");
//     }
    
//     /* Open popup */
//     $(popup).show();
    
//     /* Close popup if user clicks on background */
//     $(popup).click(function(e) {
//         if (e.target == this) {
//             if ($(popup).is(':visible')) {
//                 $(popup).hide();
//             }
//         }
//     });
    
//     /* Close popup and remove errors if user clicks on cancel or close buttons */
//     $(popup).find(".popup-btn-close").on("click", function() {
//         if ($(".formElementError").is(':visible')) {
//             $(".formElementError").remove();
//         }
//         $(popup).hide();
//     });

// }
    
// $(document).ready(function() {
//     $(".popup-trigger").on("click", function() {
// var target = $(this).data('target');
// popupOpenClose($(target));
// });
// });