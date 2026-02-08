let Google_Search_Box_Wrapper = document.getElementById("Google_Search_Box_Wrapper");
let Search_Input = document.getElementById("Google_Search_Input");

function Create_Google_Lightning() {
    for (let i = 0; i < 10; i++) {
        let Google_Lightning_Effect = document.createElement("div");
        Google_Lightning_Effect.classList.add("Google_Lightning");

        let Random_X = Math.random() * Google_Search_Box_Wrapper.offsetWidth;

        Google_Lightning_Effect.style.left = Random_X + "px";

        Google_Search_Box_Wrapper.appendChild(Google_Lightning_Effect);

        setTimeout(() => {
            Google_Lightning_Effect.remove();
        }, 170);
    }
}

Search_Input.addEventListener("input", Create_Google_Lightning);
