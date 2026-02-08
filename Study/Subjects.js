let Available_Subjects_Data = [
    {
        Subject_Name:"CSE",
        Subject_Link:"CSE"
    }
]

let Upcoming_Subjects_Data = [
    {
        Subject_Name:"Psychology"
    },
    {
        Subject_Name:"Defence"
    }
]

let Available_Grid = document.getElementById("Available_Subjects")
let Upcoming_Grid = document.getElementById("Upcoming_Subjects")

Available_Subjects_Data.forEach(Subject => {

    let Card = document.createElement("div")
    Card.className = "Subject_Card"

    Card.innerHTML = `
        <h2>${Subject.Subject_Name}</h2>
    `

    Card.onclick = function(){
        window.location.href = Subject.Subject_Link
    }

    Available_Grid.appendChild(Card)
})

Upcoming_Subjects_Data.forEach(Subject => {

    let Card = document.createElement("div")
    Card.className = "Subject_Card Upcoming"

    Card.innerHTML = `
        <h2>${Subject.Subject_Name}</h2>
    `

    Upcoming_Grid.appendChild(Card)
})