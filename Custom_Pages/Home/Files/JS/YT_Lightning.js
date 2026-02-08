let YT_Search_Box_Wrapper = document.getElementById("YT_Search_Box_Wrapper");
let YT_Search_Input = document.getElementById("YT_Search_Input");

function Create_YT_Lightning() {
    for (let i = 0; i < 10; i++) {
        let YT_Lightning_Effect = document.createElement("div");
        YT_Lightning_Effect.classList.add("YT_Lightning");

        let Random_X = Math.random() * YT_Search_Box_Wrapper.offsetWidth;

        YT_Lightning_Effect.style.left = Random_X + "px";

        YT_Search_Box_Wrapper.appendChild(YT_Lightning_Effect);

        setTimeout(() => {
            YT_Lightning_Effect.remove();
        }, 250);
    }
}

YT_Search_Input.addEventListener("input", Create_YT_Lightning);