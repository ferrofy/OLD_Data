const Topic_Colors = [
    "#3b82f6", "#8b5cf6", "#06b6d4", "#ec4899",
    "#f59e0b", "#22c55e", "#6366f1", "#14b8a6", "#a855f7"
];

function Get_Storage_Key(Topic, Task) {
    return "DET__" + Topic + "__" + Task;
}

function Is_Done(Topic, Task) {
    return localStorage.getItem(Get_Storage_Key(Topic, Task)) === "true";
}

function Set_Done(Topic, Task, Value) {
    localStorage.setItem(Get_Storage_Key(Topic, Task), Value ? "true" : "false");
}

function Count_Done_In_Topic(Topic) {
    return Roadmap[Topic].Tasks.filter(T => Is_Done(Topic, T)).length;
}

function Count_Total_In_Topic(Topic) {
    return Roadmap[Topic].Tasks.length;
}

function Count_All_Done() {
    return Object.keys(Roadmap).reduce((Sum, T) => Sum + Count_Done_In_Topic(T), 0);
}

function Count_All_Total() {
    return Object.keys(Roadmap).reduce((Sum, T) => Sum + Count_Total_In_Topic(T), 0);
}
