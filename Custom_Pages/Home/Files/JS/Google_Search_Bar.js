window.addEventListener("load", function() {

    let Google_Search_Input = document.getElementById("Google_Search_Input")
    let Google_Search_Button = document.getElementById("Google_Search_Button")
    let Google_Search_Result = document.getElementById("Google_Search_Result")

    function Execute_Google_Search() {
        let Google_Search_Text = Google_Search_Input.value.trim()

        if(Google_Search_Text === "") {
            Google_Search_Result.innerText = ""
            return
        }

        Google_Search_Result.innerText = ""

        let Google_Url = "https://www.google.com/search?q=" + encodeURIComponent(Google_Search_Text)

        window.location.href = Google_Url
    }

    Google_Search_Button.addEventListener("click", Execute_Google_Search)

    Google_Search_Input.addEventListener("keydown", function(Event_Key) {
        if(Event_Key.key === "Enter") {
            Execute_Google_Search()
        }
    })

})
