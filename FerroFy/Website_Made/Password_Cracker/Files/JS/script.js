let Num_Chars = "0123456789";
let Lower_Chars = "abcdefghijklmnopqrstuvwxyz";
let Upper_Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let Special_Chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~\"\\ ";

let Char_Sets = {
    "All_Mix": Num_Chars + Lower_Chars + Upper_Chars + Special_Chars,
    "Numbers_Only": Num_Chars,
    "Alphabet_Both": Lower_Chars + Upper_Chars,
    "Alphabet_Upper": Upper_Chars,
    "Alphabet_Lower": Lower_Chars,
    "Special_Only": Special_Chars,
    "Mix_Num_Alphabet_Both": Num_Chars + Lower_Chars + Upper_Chars,
    "Mix_Num_Alphabet_Upper": Num_Chars + Upper_Chars,
    "Mix_Num_Alphabet_Lower": Num_Chars + Lower_Chars,
    "Mix_Alphabet_Special": Lower_Chars + Upper_Chars + Special_Chars
};

let Char_Set = Char_Sets["All_Mix"];
let Target_Password = "";
let Is_Running = false;
let Start_Time = 0;
let Current_Length = 1;
let Current_Indexes = [];
let Total_Attempts = 0;
let Animation_Frame_Id = null;
let Batch_Size = 25000;
let Uploaded_Passwords = null;

function Update_Time_Display() {
    let Current_Time = performance.now();
    let Time_Diff = Current_Time - Start_Time;
    let Hours = Math.floor((Time_Diff / (1000 * 60 * 60)) % 24);
    let Minutes = Math.floor((Time_Diff / 1000 / 60) % 60);
    let Seconds = Math.floor((Time_Diff / 1000) % 60);
    let Milliseconds = Math.floor(Time_Diff % 1000);
    
    let Formatted_Hours = String(Hours).padStart(2, '0');
    let Formatted_Minutes = String(Minutes).padStart(2, '0');
    let Formatted_Seconds = String(Seconds).padStart(2, '0');
    let Formatted_Milliseconds = String(Milliseconds).padStart(3, '0');
    
    document.getElementById("Time_Display").innerText = `${Formatted_Hours}:${Formatted_Minutes}:${Formatted_Seconds}.${Formatted_Milliseconds}`;
    
    let Speed = 0;
    if (Time_Diff > 0) {
        Speed = Math.floor(Total_Attempts / (Time_Diff / 1000));
    }
    document.getElementById("Speed_Display").innerText = Speed.toLocaleString();
}

function Start_Cracking() {
    Target_Password = document.getElementById("Password_Input").value;
    if (Target_Password === "") {
        document.getElementById("Status_Text").innerText = "System Error : Enter Target First!";
        document.getElementById("Status_Text").style.color = "#ff0055";
        return;
    }
    
    document.getElementById("Start_Button").style.pointerEvents = "none";
    document.getElementById("Start_Button").style.opacity = "0.5";
    document.getElementById("Password_Input").disabled = true;
    document.getElementById("File_Input").disabled = true;
    document.getElementById("Char_Set_Selector").disabled = true;
    
    let Selected_Mode = document.getElementById("Char_Set_Selector").value;
    Char_Set = Char_Sets[Selected_Mode];
    
    Is_Running = true;
    Start_Time = performance.now();
    Total_Attempts = 0;
    
    if (Uploaded_Passwords && Uploaded_Passwords.length > 0) {
        document.getElementById("Status_Text").innerText = "System Status : Rainbow Attack In Progress...";
        document.getElementById("Status_Text").style.color = "#00ffcc";
        document.getElementById("Status_Text").style.textShadow = "0 0 10px #00ffcc";
        Run_Rainbow_Attack(Uploaded_Passwords, 0);
    } else {
        Current_Length = 1;
        Current_Indexes = [0];
        document.getElementById("Status_Text").innerText = "System Status : Bruteforcing In Progress...";
        document.getElementById("Status_Text").style.color = "#00ffcc";
        document.getElementById("Status_Text").style.textShadow = "0 0 10px #00ffcc";
        Run_Bruteforce_Batch();
    }
}

function Stop_Cracking() {
    Is_Running = false;
    document.getElementById("Status_Text").innerText = "System Status : Idle";
    document.getElementById("Status_Text").style.color = "#888";
    document.getElementById("Status_Text").style.textShadow = "none";
    
    document.getElementById("Start_Button").style.pointerEvents = "all";
    document.getElementById("Start_Button").style.opacity = "1";
    document.getElementById("Password_Input").disabled = false;
    document.getElementById("File_Input").disabled = false;
    document.getElementById("Char_Set_Selector").disabled = false;
}

function Run_Bruteforce_Batch() {
    if (!Is_Running) {
        return;
    }
    
    let Is_Found = false;
    let Current_Guess = "";
    
    for (let Step = 0; Step < Batch_Size; Step++) {
        Current_Guess = "";
        for (let Index = 0; Index < Current_Length; Index++) {
            Current_Guess += Char_Set[Current_Indexes[Index]];
        }
        
        Total_Attempts++;
        
        if (Current_Guess === Target_Password) {
            Is_Found = true;
            break;
        }
        
        let Carry_Over = true;
        for (let Index = Current_Length - 1; Index >= 0; Index--) {
            if (Carry_Over) {
                Current_Indexes[Index]++;
                if (Current_Indexes[Index] >= Char_Set.length) {
                    Current_Indexes[Index] = 0;
                    Carry_Over = true;
                } else {
                    Carry_Over = false;
                }
            }
        }
        
        if (Carry_Over) {
            Current_Length++;
            Current_Indexes = new Array(Current_Length).fill(0);
        }
    }
    
    Update_Time_Display();
    document.getElementById("Attempts_Display").innerText = Total_Attempts.toLocaleString();
    document.getElementById("Guess_Display").innerText = Current_Guess;
    
    if (Is_Found) {
        Is_Running = false;
        document.getElementById("Status_Text").innerText = "System Status : Password Cracked!";
        document.getElementById("Status_Text").style.color = "#ff0055";
        document.getElementById("Status_Text").style.textShadow = "0 0 10px #ff0055";
        
        document.getElementById("Start_Button").style.pointerEvents = "all";
        document.getElementById("Start_Button").style.opacity = "1";
        document.getElementById("Password_Input").disabled = false;
        return;
    }
    
    Animation_Frame_Id = requestAnimationFrame(Run_Bruteforce_Batch);
}

function Handle_File_Upload(Event) {
    let File = Event.target.files[0];
    if (!File) {
        Uploaded_Passwords = null;
        return;
    }

    let Reader = new FileReader();
    Reader.onload = function(E) {
        let Content = E.target.result;
        Uploaded_Passwords = Content.split(/\r?\n/);
        
        document.getElementById("Status_Text").innerText = "System Status : Dictionary File Loaded. Ready To Attack.";
        document.getElementById("Status_Text").style.color = "#00ffcc";
    };
    Reader.readAsText(File);
}

function Run_Rainbow_Attack(Passwords, Current_Index) {
    if (!Is_Running) return;
    
    let Is_Found = false;
    let Current_Guess = "";
    
    let End_Index = Math.min(Current_Index + Batch_Size, Passwords.length);
    
    for (let Index = Current_Index; Index < End_Index; Index++) {
        Current_Guess = Passwords[Index];
        Total_Attempts++;
        
        if (Current_Guess === Target_Password) {
            Is_Found = true;
            break;
        }
    }
    
    Update_Time_Display();
    document.getElementById("Attempts_Display").innerText = Total_Attempts.toLocaleString();
    document.getElementById("Guess_Display").innerText = Current_Guess;
    
    if (Is_Found) {
        Is_Running = false;
        document.getElementById("Status_Text").innerText = "System Status : Password Cracked via Dictionary!";
        document.getElementById("Status_Text").style.color = "#ff0055";
        document.getElementById("Status_Text").style.textShadow = "0 0 10px #ff0055";
        
        Reset_UI();
        return;
    }
    
    if (End_Index >= Passwords.length) {
        Is_Running = false;
        document.getElementById("Status_Text").innerText = "System Status : Attack Failed. Target Not In File.";
        document.getElementById("Status_Text").style.color = "#888";
        document.getElementById("Status_Text").style.textShadow = "none";
        Reset_UI();
        return;
    }
    
    Animation_Frame_Id = requestAnimationFrame(() => Run_Rainbow_Attack(Passwords, End_Index));
}

function Reset_UI() {
    document.getElementById("Start_Button").style.pointerEvents = "all";
    document.getElementById("Start_Button").style.opacity = "1";
    document.getElementById("Password_Input").disabled = false;
    document.getElementById("File_Input").disabled = false;
    document.getElementById("Char_Set_Selector").disabled = false;
    document.getElementById("File_Input").value = "";
    Uploaded_Passwords = null;
}

document.getElementById("Start_Button").addEventListener("click", Start_Cracking);
document.getElementById("Stop_Button").addEventListener("click", Stop_Cracking);
document.getElementById("File_Input").addEventListener("change", Handle_File_Upload);
