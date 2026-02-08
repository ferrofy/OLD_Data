let Search_Slider_Track = document.getElementById("Search_Slider_Track");

function Show_Panel(Index_Value) {
    let Screen_Width = window.innerWidth
    let Move_X = Index_Value * -Screen_Width
    Search_Slider_Track.style.transform = "translateX(" + Move_X + "px)";
}
