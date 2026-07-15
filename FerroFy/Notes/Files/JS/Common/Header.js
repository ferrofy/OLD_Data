let Nav_Items_List = [
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

let Click = 0
let Header_El = document.querySelector("header")
let Menu_Bar = document.getElementById("Menu_Bar")
let Menu_Side_Bar = document.getElementById("Menu_Side_Bar")
let Nav_Bar_Heading = document.getElementById("Header_Nav")
let Nav_Bar_Menu = document.getElementById("Menu_Nav")
let Menu_Overlay = document.getElementById("Menu_Overlay")

for (let Index = 0; Index < Nav_Items_List.length; Index++) {

    let Item_Header = document.createElement("a")
    let Item_Menu = document.createElement("a")

    Item_Header.textContent = Nav_Items_List[Index].Title
    Item_Menu.textContent = Nav_Items_List[Index].Title

    Item_Header.href = Nav_Items_List[Index].href
    Item_Menu.href = Nav_Items_List[Index].href

    Nav_Bar_Heading.appendChild(Item_Header)
    Nav_Bar_Menu.appendChild(Item_Menu)
}

window.addEventListener("scroll", function () {
    if (window.scrollY > 10) {
        Header_El.classList.add("Header_Scrolled")
    } else {
        Header_El.classList.remove("Header_Scrolled")
    }
})

Menu_Overlay.addEventListener("click", function () {
    Close_Menu()
})

function Close_Menu() {
    Menu_Side_Bar.style.display = "none"
    Menu_Side_Bar.classList.remove("Menu_Open")
    Menu_Overlay.classList.remove("Menu_Open")
    Menu_Bar.classList.remove("Menu_Open")
    Click = 0
}

function Open_Menu() {
    Menu_Side_Bar.style.display = "flex"

    requestAnimationFrame(function () {
        Menu_Side_Bar.classList.add("Menu_Open")
        Menu_Overlay.classList.add("Menu_Open")
        Menu_Bar.classList.add("Menu_Open")
    })
}

Menu_Bar.addEventListener("click", function () {
    Click++
    if ((Click % 2) == 1) {
        Open_Menu()
    }
    else {
        Close_Menu()
    }
})