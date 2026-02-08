window.addEventListener("load", function() {

    let Chat_GPT_Search_Input = document.getElementById("Chat_GPT_Search_Input")
    let Chat_GPT_Search_Button = document.getElementById("Chat_GPT_Search_Button")
    let Chat_GPT_Search_Result = document.getElementById("Chat_GPT_Search_Result")

    function Execute_Chat_GPT_Search() {
        let Chat_GPT_Search_Text = Chat_GPT_Search_Input.value.trim()

        if(Chat_GPT_Search_Text === "") {
            Chat_GPT_Search_Result.innerText = ""
            return
        }

        Chat_GPT_Search_Result.innerText = ""

        let Chat_GPT_Url = "https://chat.openai.com/?q=" + encodeURIComponent(Chat_GPT_Search_Text)

        window.location.href = Chat_GPT_Url
    }

    Chat_GPT_Search_Button.addEventListener("click", Execute_Chat_GPT_Search)

    Chat_GPT_Search_Input.addEventListener("keydown", function(Event_Key) {

        if(Event_Key.key === "Enter" && !Event_Key.shiftKey) {
            Event_Key.preventDefault()
            Chat_GPT_Search_Button.click()
        }

    })

})