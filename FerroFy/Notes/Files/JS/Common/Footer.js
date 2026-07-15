let Quick_Link_List = [
    {
        Title: "HOME",
        href: "#"
    },
    {
        Title: "CSE",
        href: "#"
    },
    {
        Title: "PHYSICS",
        href: "#"
    },
    {
        Title: "MATH",
        href: "#"
    },
];


let Footer_Quick_Link = document.getElementById("Quick_Link")
const Icon_Share = document.getElementById("Icon_Share");

for (let Index = 0; Index < Quick_Link_List.length; Index++) {

    let Item = document.createElement("a")

    Item.textContent = Quick_Link_List[Index].Title
    Item.href = Quick_Link_List[Index].href

    Footer_Quick_Link.appendChild(Item)
}


Icon_Share.addEventListener("click", () => {
    navigator.clipboard.writeText(window.location.href).then(() => {
        Copy_PopUp();
    });
});

function Copy_PopUp() {
    const Existing = document.getElementById("Copy_PopUp");
    if (Existing) Existing.remove();

    const Copy_PopUp = document.createElement("div");
    Copy_PopUp.id = "Copy_PopUp";
    Copy_PopUp.textContent = "Copied The Page Link!";
    document.body.appendChild(Copy_PopUp);

    setTimeout(() => {
        Copy_PopUp.classList.add("Copy_PopUp_Hide");
        setTimeout(() => Copy_PopUp.remove(), 400);
    }, 1000);
}
