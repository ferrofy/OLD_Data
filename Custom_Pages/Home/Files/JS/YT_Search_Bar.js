window.addEventListener("load", function() {

    let YT_Search_Input = document.getElementById("YT_Search_Input")
    let YT_Search_Button = document.getElementById("YT_Search_Button")
    let YT_Search_Result = document.getElementById("YT_Search_Result")

    function Execute_Search() {
        let YT_Search_Text = YT_Search_Input.value.trim()

        if(YT_Search_Text === "") {
            YT_Search_Result.innerText = ""
            return
        }

        YT_Search_Result.innerText = ""

        let YT_Url = "https://www.Youtube.com/search?q=" + encodeURIComponent(YT_Search_Text)

        window.location.href = YT_Url
    }

    YT_Search_Button.addEventListener("click", Execute_Search)

    YT_Search_Input.addEventListener("keydown", function(Event_Key) {
        if(Event_Key.key === "Enter") {
            Execute_Search()
        }
    })

})
