let Shortcut_Database = [
    { Title: "Linux", Link: "https://www.youtube.com/playlist?list=PLJ9KaYo7PXTDJwBDJaikgTsEGnL7KBeyC" },
    { Title: "OS", Link: "https://www.youtube.com/playlist?list=PLJ9KaYo7PXTCCekllSlLmM3c7sGkxHv4J" },
    { Title: "Python", Link: "https://www.youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg" },
    { Title: "WebDev", Link: "https://www.youtube.com/playlist?list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w" },
    { Title: "SQL", Link: "https://www.youtube.com/playlist?list=PLJ9KaYo7PXTC66uDTZpqD4ojDA-xt5Krx" },
    { Title: "Java", Link: "https://www.youtube.com/playlist?list=PLu0W_9lII9agS67Uits0UnJyrYiXhDS6q" },
    { Title: "C Lang", Link: "https://www.youtube.com/playlist?list=PLu0W_9lII9aiXlHcLx-mDH1Qul38wD3aR" },
    { Title: "Git", Link: "https://www.youtube.com/playlist?list=PLu0W_9lII9agwhy658ZPA0MTStKUJTWPi" },
    { Title: "Bash Chunk", Link: "https://www.youtube.com/playlist?list=PLIhvC56v63IKioClkSNDjW7iz-6TFvLwS" },
    { Title: "Linux Chunk", Link: "https://www.youtube.com/playlist?list=PLIhvC56v63IL2OjFvv_PI0B2yAXGfJLMI" },
    { Title: "Linux 2 Chunk", Link: "https://www.youtube.com/playlist?list=PLIhvC56v63IJIujb5cyE13oLuyORZpdkL" },
    { Title: "Hacking Chunk", Link: "https://www.youtube.com/playlist?list=PLIhvC56v63IIJZRa3lzK6IeBQOH_VFjUQ" },
];

let Shortcut_Row = document.getElementById("Shortcut_Row");

function Build_Shortcuts() {
    Shortcut_Row.innerHTML = "";

    Shortcut_Database.forEach(Item => {
        let Shortcut_Card = document.createElement("div");
        Shortcut_Card.className = "Shortcut_Card";

        Shortcut_Card.innerHTML = `
            <div class="Shortcut_Icon">
                <div class="YT_Circle">
                    <div class="YT_Play_Back">
                        <div class="YT_Play_Triangle"></div>
                    </div>
                </div>
            </div>
            <p>${Item.Title}</p>
        `;

        Shortcut_Card.onclick = () => window.open(Item.Link, "_self");

        Shortcut_Row.appendChild(Shortcut_Card);
    });
}

Build_Shortcuts();