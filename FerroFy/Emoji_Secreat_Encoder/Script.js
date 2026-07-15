const VS_BASE = 0xE0100;

function encode() {

    let emojis = document.getElementById("emojiInput").value;
    let secret = document.getElementById("secretInput").value;

    let encoded = emojis;

    for (let i = 0; i < secret.length; i++) {

        let code = secret.charCodeAt(i);

        encoded += String.fromCodePoint(VS_BASE + code);

    }

    document.getElementById("encoded").innerText = encoded;

}
function decode() {

    let input = document.getElementById("decodeInput").value;

    let message = "";

    for (let char of input) {

        let code = char.codePointAt(0);

        if (code >= VS_BASE && code <= VS_BASE + 255) {

            message += String.fromCharCode(code - VS_BASE);

        }

    }

    document.getElementById("decoded").innerText = message || "No hidden message found";

}

function copyEncoded() {

    let text = document.getElementById("encoded").innerText;

    navigator.clipboard.writeText(text).then(() => {
        alert("Encrypted emojis copied!");
    });

}