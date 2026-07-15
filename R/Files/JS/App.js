function Safe_Id(Topic) {
    return Topic.replace(/\s+/g, "_").replace(/[^a-zA-Z0-9_]/g, "");
}

function Make_Check_Svg() {
    return `<svg width="11" height="9" viewBox="0 0 11 9" fill="none">
        <path d="M1 4L4 7L10 1" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
}

function Make_Chevron_Svg() {
    return `<svg width="12" height="12" viewBox="0 0 12 12" fill="none">
        <path d="M2 4L6 8L10 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
}

function Build_Task_Item(Topic, Task_Name) {
    const Done = Is_Done(Topic, Task_Name);
    const Item = document.createElement("label");
    Item.className = "Task_Item" + (Done ? " Completed" : "");
    Item.innerHTML = `
        <div class="Custom_Check">${Done ? Make_Check_Svg() : ""}</div>
        <input type="checkbox" class="Task_Real_Check" ${Done ? "checked" : ""}>
        <span class="Task_Text">${Task_Name}</span>
        <span class="Task_Done_Tag">Done</span>
    `;

    const Real_Check = Item.querySelector(".Task_Real_Check");
    const Custom_Box = Item.querySelector(".Custom_Check");

    Item.addEventListener("click", function (E) {
        E.preventDefault();
        const New_State = !Real_Check.checked;
        Real_Check.checked = New_State;
        Set_Done(Topic, Task_Name, New_State);

        if (New_State) {
            Item.classList.add("Completed");
            Custom_Box.innerHTML = Make_Check_Svg();
        } else {
            Item.classList.remove("Completed");
            Custom_Box.innerHTML = "";
        }

        Refresh_All(Topic);
    });

    return Item;
}

function Build_Topic_Card(Topic, Index) {
    const Info = Roadmap[Topic];
    const Color = Info.Color;
    const Safe = Safe_Id(Topic);
    const Total = Count_Total_In_Topic(Topic);
    const Done = Count_Done_In_Topic(Topic);
    const Pct = Total > 0 ? Math.round((Done / Total) * 100) : 0;

    const Card = document.createElement("div");
    Card.className = "Topic_Card Collapsed";
    Card.id = "Card_" + Safe;

    Card.innerHTML = `
        <div class="Topic_Header" id="Hdr_${Safe}">
            <div class="Topic_Header_Left">
                <div class="Topic_Icon" style="background:${Color}18; color:${Color};">
                    ${Info.Icon}
                </div>
                <div class="Topic_Name_Wrap">
                    <div class="Topic_Name">${Topic}</div>
                    <div class="Topic_Sub_Count">${Total} Topics</div>
                </div>
            </div>
            <div class="Topic_Header_Right">
                <div class="Topic_Mini_Chart">
                    <canvas id="Mini_${Safe}"></canvas>
                    <div class="Topic_Mini_Pct" id="Mini_Pct_${Safe}">${Pct}%</div>
                </div>
                <div class="Topic_Chevron">${Make_Chevron_Svg()}</div>
            </div>
        </div>
        <div class="Topic_Progress_Strip">
            <div class="Topic_Progress_Track">
                <div class="Topic_Progress_Fill" id="TBar_${Safe}"
                    style="width:${Pct}%; background:${Color};">
                </div>
            </div>
        </div>
        <div class="Topic_Body" id="Body_${Safe}">
            <div class="Topic_Body_Row">
                <div class="Tasks_List" id="List_${Safe}"></div>
                <div class="Topic_Chart_Side">
                    <div class="Topic_Chart_Canvas_Wrap">
                        <canvas id="Chart_${Safe}"></canvas>
                        <div class="Topic_Chart_Center" id="Ctr_${Safe}">${Pct}%</div>
                    </div>
                    <div class="Topic_Chart_Stat" id="Stat_${Safe}">${Done}/${Total} Done</div>
                </div>
            </div>
        </div>
    `;

    const Hdr = Card.querySelector(".Topic_Header");
    Hdr.addEventListener("click", () => Toggle_Topic(Safe, Card));

    return Card;
}

function Toggle_Topic(Safe, Card) {
    const Body = document.getElementById("Body_" + Safe);
    const Is_Collapsed = Card.classList.contains("Collapsed");

    if (Is_Collapsed) {
        Card.classList.remove("Collapsed");
        Body.style.maxHeight = Body.scrollHeight + "px";
        Body.style.opacity = "1";
        Body.style.paddingTop = "";
        Body.style.paddingBottom = "";
    } else {
        Body.style.maxHeight = "0";
        Body.style.opacity = "0";
        Body.style.paddingTop = "0";
        Body.style.paddingBottom = "0";
        Card.classList.add("Collapsed");
    }
}

function Refresh_All(Topic) {
    const Info = Roadmap[Topic];
    const Color = Info.Color;
    const Safe = Safe_Id(Topic);
    const Total = Count_Total_In_Topic(Topic);
    const Done = Count_Done_In_Topic(Topic);
    const Pct = Total > 0 ? Math.round((Done / Total) * 100) : 0;

    const T_Bar = document.getElementById("TBar_" + Safe);
    if (T_Bar) T_Bar.style.width = Pct + "%";

    const Mini_Pct = document.getElementById("Mini_Pct_" + Safe);
    if (Mini_Pct) Mini_Pct.textContent = Pct + "%";

    const Ctr = document.getElementById("Ctr_" + Safe);
    if (Ctr) Ctr.textContent = Pct + "%";

    const Stat = document.getElementById("Stat_" + Safe);
    if (Stat) Stat.textContent = Done + "/" + Total + " Done";

    Refresh_Topic_Charts(Topic);

    const All_Done = Count_All_Done();
    const All_Total = Count_All_Total();
    const All_Pct = All_Total > 0 ? Math.round((All_Done / All_Total) * 100) : 0;

    const Main_Pct_El = document.getElementById("Main_Pct");
    if (Main_Pct_El) Main_Pct_El.textContent = All_Pct + "%";

    const Main_Bar = document.getElementById("Main_Bar");
    if (Main_Bar) Main_Bar.style.width = All_Pct + "%";

    const Done_Count_El = document.getElementById("Done_Count");
    if (Done_Count_El) Done_Count_El.textContent = All_Done;

    const Left_Count_El = document.getElementById("Left_Count");
    if (Left_Count_El) Left_Count_El.textContent = All_Total - All_Done;

    const Prog_Count = document.getElementById("Prog_Count");
    if (Prog_Count) Prog_Count.textContent = All_Done + " / " + All_Total;

    Refresh_Main_Chart();
    Update_Legend();
    Update_Timer_Display();
}

function Update_Legend() {
    const Topics = Object.keys(Roadmap);
    Topics.forEach(Topic => {
        const Safe = Safe_Id(Topic);
        const Done = Count_Done_In_Topic(Topic);
        const Total = Count_Total_In_Topic(Topic);
        const Pct = Total > 0 ? Math.round((Done / Total) * 100) : 0;
        const El = document.getElementById("Leg_" + Safe);
        if (El) El.textContent = Pct + "%";
    });
}

function Init_All() {
    Init_Main_Chart();

    const All_Done = Count_All_Done();
    const All_Total = Count_All_Total();
    const All_Pct = All_Total > 0 ? Math.round((All_Done / All_Total) * 100) : 0;

    document.getElementById("Main_Pct").textContent = All_Pct + "%";
    document.getElementById("Main_Bar").style.width = All_Pct + "%";
    document.getElementById("Done_Count").textContent = All_Done;
    document.getElementById("Left_Count").textContent = All_Total - All_Done;
    document.getElementById("Prog_Count").textContent = All_Done + " / " + All_Total;

    Refresh_Main_Chart();
    Update_Chart_Data(Chart_Registry["__main__"], All_Done, All_Total);

    const Topics_Col = document.getElementById("Topics_Col");
    const Legend_List = document.getElementById("Legend_List");

    Object.keys(Roadmap).forEach((Topic, Index) => {
        const Info = Roadmap[Topic];
        const Color = Info.Color;
        const Safe = Safe_Id(Topic);
        const Total = Count_Total_In_Topic(Topic);
        const Done = Count_Done_In_Topic(Topic);
        const Pct = Total > 0 ? Math.round((Done / Total) * 100) : 0;

        const Card = Build_Topic_Card(Topic, Index);
        Topics_Col.appendChild(Card);

        const List_El = document.getElementById("List_" + Safe);
        Info.Tasks.forEach(Task_Name => {
            List_El.appendChild(Build_Task_Item(Topic, Task_Name));
        });

        const Body_El = document.getElementById("Body_" + Safe);
        Body_El.style.maxHeight = "0";
        Body_El.style.opacity = "0";
        Body_El.style.paddingTop = "0";
        Body_El.style.paddingBottom = "0";

        setTimeout(() => {
            Init_Mini_Chart(Topic, Color);
            Init_Topic_Chart(Topic, Color);
            Update_Chart_Data(Chart_Registry[Topic], Done, Total);
            Update_Chart_Data(Chart_Registry["mini_" + Topic], Done, Total);
        }, 50 + Index * 30);

        const Leg_Item = document.createElement("div");
        Leg_Item.className = "Legend_Item";
        Leg_Item.innerHTML = `
            <div class="Legend_Left">
                <div class="Legend_Dot" style="background:${Color};"></div>
                <span class="Legend_Name">${Topic}</span>
            </div>
            <span class="Legend_Pct" id="Leg_${Safe}">${Pct}%</span>
        `;
        Legend_List.appendChild(Leg_Item);
    });

    Start_Timer();
}

document.addEventListener("DOMContentLoaded", Init_All);
