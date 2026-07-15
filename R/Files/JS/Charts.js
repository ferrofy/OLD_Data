const Chart_Registry = {};

function Safe_Canvas_Id(Topic) {
    return Topic.replace(/\s+/g, "_").replace(/[^a-zA-Z0-9_]/g, "");
}

const Main_Chart_Config = {
    type: "doughnut",
    data: {
        labels: ["Completed", "Remaining"],
        datasets: [{
            data: [0, 1],
            backgroundColor: ["#22c55e", "rgba(255,255,255,0.05)"],
            borderColor: ["rgba(34,197,94,0.6)", "rgba(255,255,255,0.04)"],
            borderWidth: 1,
            hoverOffset: 6
        }]
    },
    options: {
        cutout: "78%",
        animation: { animateRotate: true, duration: 700, easing: "easeInOutQuart" },
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function (ctx) {
                        return " " + ctx.label + ": " + ctx.raw;
                    }
                },
                backgroundColor: "rgba(10,15,30,0.95)",
                titleColor: "#94a3b8",
                bodyColor: "#f1f5f9",
                borderColor: "rgba(255,255,255,0.08)",
                borderWidth: 1,
                padding: 10,
                cornerRadius: 10
            }
        }
    }
};

function Make_Topic_Chart_Config(Color) {
    return {
        type: "doughnut",
        data: {
            labels: ["Done", "Left"],
            datasets: [{
                data: [0, 1],
                backgroundColor: [Color, "rgba(255,255,255,0.05)"],
                borderColor: [Color + "99", "rgba(255,255,255,0.04)"],
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            cutout: "70%",
            animation: { animateRotate: true, duration: 600, easing: "easeInOutQuart" },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (ctx) { return " " + ctx.label + ": " + ctx.raw; }
                    },
                    backgroundColor: "rgba(10,15,30,0.95)",
                    titleColor: "#94a3b8",
                    bodyColor: "#f1f5f9",
                    borderColor: "rgba(255,255,255,0.08)",
                    borderWidth: 1,
                    padding: 8,
                    cornerRadius: 8
                }
            }
        }
    };
}

function Update_Chart_Data(Chart_Obj, Done, Total) {
    Chart_Obj.data.datasets[0].data = [Done, Total - Done];
    Chart_Obj.update("active");
}

function Init_Main_Chart() {
    const Canvas = document.getElementById("Main_Chart");
    Chart_Registry["__main__"] = new Chart(Canvas, Main_Chart_Config);
}

function Refresh_Main_Chart() {
    const Done = Count_All_Done();
    const Total = Count_All_Total();
    const Chart_Obj = Chart_Registry["__main__"];
    if (Chart_Obj) Update_Chart_Data(Chart_Obj, Done, Total);
}

function Init_Topic_Chart(Topic, Color) {
    const Canvas = document.getElementById("Chart_" + Safe_Canvas_Id(Topic));
    if (!Canvas) return;
    if (Chart_Registry[Topic]) Chart_Registry[Topic].destroy();
    Chart_Registry[Topic] = new Chart(Canvas, Make_Topic_Chart_Config(Color));
}

function Init_Mini_Chart(Topic, Color) {
    const Canvas = document.getElementById("Mini_" + Safe_Canvas_Id(Topic));
    if (!Canvas) return;
    if (Chart_Registry["mini_" + Topic]) Chart_Registry["mini_" + Topic].destroy();
    Chart_Registry["mini_" + Topic] = new Chart(Canvas, Make_Topic_Chart_Config(Color));
}

function Refresh_Topic_Charts(Topic) {
    const Done = Count_Done_In_Topic(Topic);
    const Total = Count_Total_In_Topic(Topic);
    const Chart_Obj = Chart_Registry[Topic];
    const Mini_Obj = Chart_Registry["mini_" + Topic];
    if (Chart_Obj) Update_Chart_Data(Chart_Obj, Done, Total);
    if (Mini_Obj) Update_Chart_Data(Mini_Obj, Done, Total);
}
