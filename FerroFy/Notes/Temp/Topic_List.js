const Topics = {
    "Basic Tools / About System": [
        { Name: "Sample 1", Icon: "fa-solid fa-code" }
    ],

    "Programming / Scripting Languages": [
        { Name: "Sample 2", Icon: "fa-brands fa-html5" }
    ],

    "Fields": [
        { Name: "Sample 3", Icon: "fa-solid fa-shield-halved" }
    ]
};


const Section_Mapping = {
    "Basic Tools / About System": "Tools_Cards",
    "Programming / Scripting Languages": "Languages_Cards",
    "Fields": "Fields_Cards"
};


Object.keys(Topics).forEach(Section_Name => {
    const Container_Id = Section_Mapping[Section_Name];
    const Container = document.getElementById(Container_Id);

    if (Container) {
        Topics[Section_Name].forEach(Topic => {
            const Card = document.createElement("a");

            Card.href = "#";
            Card.className = "Topic_Card";

            Card.innerHTML = `
                <div class="Topic_Icon">
                    <i class="${Topic.Icon}"></i>
                </div>

                <div class="Topic_Name">
                    ${Topic.Name}
                </div>

                <div class="Topic_Tag">
                    Topic
                </div>
            `;

            Container.appendChild(Card);
        });
    }
});


const Search_Input = document.getElementById("Search_Input");


if (Search_Input) {
    Search_Input.addEventListener("input", function () {
        const Query = Search_Input.value
            .toLowerCase()
            .trim();

        const All_Cards = document.querySelectorAll(".Topic_Card");

        All_Cards.forEach(Card => {
            const Name = Card
                .querySelector(".Topic_Name")
                ?.textContent
                .toLowerCase() || "";

            const Tag = Card
                .querySelector(".Topic_Tag")
                ?.textContent
                .toLowerCase() || "";

            const Match =
                Name.includes(Query) ||
                Tag.includes(Query);

            Card.classList.toggle(
                "Hidden_Card",
                Query.length > 0 && !Match
            );
        });


        document
            .querySelectorAll(".Topic_Section")
            .forEach(Section => {
                const Visible_Cards =
                    Section.querySelectorAll(
                        ".Topic_Card:not(.Hidden_Card)"
                    ).length;

                Section.style.display =
                    Visible_Cards === 0 &&
                    Query.length > 0
                        ? "none"
                        : "";
            });
    });
}