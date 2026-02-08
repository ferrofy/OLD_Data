let Chat_GPT_Search_Box_Wrapper = document.getElementById("Chat_GPT_Search_Box_Wrapper");
let Chat_GPT_Search_Input = document.getElementById("Chat_GPT_Search_Input");

function Create_Chat_GPT_Lightning() {
    for (let i = 0; i < 10; i++) {
        let Chat_GPT_Lightning_Effect = document.createElement("div");
        Chat_GPT_Lightning_Effect.classList.add("Chat_GPT_Lightning");

        let Random_X = Math.random() * Chat_GPT_Search_Box_Wrapper.offsetWidth;

        Chat_GPT_Lightning_Effect.style.left = Random_X + "px";

        Chat_GPT_Search_Box_Wrapper.appendChild(Chat_GPT_Lightning_Effect);

        setTimeout(() => {
            Chat_GPT_Lightning_Effect.remove();
        }, 250);
    }
}

Chat_GPT_Search_Input.addEventListener("input", Create_Chat_GPT_Lightning);