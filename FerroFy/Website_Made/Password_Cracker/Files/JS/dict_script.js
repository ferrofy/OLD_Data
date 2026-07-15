let Generated_Lines = [];

function Generate_Combinations() {
    let Name_Str = document.getElementById("Dict_Name").value.trim();
    let Mobile_Str = document.getElementById("Dict_Mobile").value.trim();
    let DOB_Str = document.getElementById("Dict_DOB").value.trim();
    let Keywords_Str = document.getElementById("Dict_Keywords").value.trim();

    let Base_Words = new Set();
    
    function Get_Case_Variations(Word) {
        let Results = [];
        let Total_Permutations = 1 << Word.length;
        for (let I = 0; I < Total_Permutations; I++) {
            let Variant = "";
            for (let J = 0; J < Word.length; J++) {
                if (I & (1 << J)) {
                    Variant += Word[J].toUpperCase();
                } else {
                    Variant += Word[J].toLowerCase();
                }
            }
            Results.push(Variant);
        }
        return Results;
    }

    function Add_Word(Word) {
        if (!Word) return;
        if (Word.length <= 10) {
            let Variations = Get_Case_Variations(Word);
            Variations.forEach(V => Base_Words.add(V));
        } else {
            Base_Words.add(Word);
            Base_Words.add(Word.toLowerCase());
            Base_Words.add(Word.toUpperCase());
            Base_Words.add(Word.charAt(0).toUpperCase() + Word.slice(1).toLowerCase());
        }
    }

    if (Name_Str) {
        let Name_Parts = Name_Str.split(" ");
        Name_Parts.forEach(Add_Word);
        if (Name_Parts.length > 1) {
            Add_Word(Name_Parts.join(""));
            Add_Word(Name_Parts.join("_"));
            Add_Word(Name_Parts.join("-"));
        }
    }

    if (Mobile_Str) {
        Base_Words.add(Mobile_Str);
    }
    
    if (DOB_Str) {
        let Parts = DOB_Str.split("-");
        if (Parts.length === 3) {
            let Y = Parts[0];
            let M = Parts[1];
            let D = Parts[2];
            let M_Num = parseInt(M, 10).toString();
            let D_Num = parseInt(D, 10).toString();
            
            let Months_Short = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
            let Months_Long = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];
            
            let M_Idx = parseInt(M, 10) - 1;
            let M_Short = Months_Short[M_Idx];
            let M_Long = Months_Long[M_Idx];
            let Y_Short = Y.slice(-2);
            
            let Date_Variations = [
                D_Num + M_Num + Y,
                D + M + Y,
                D_Num + M_Num + Y_Short,
                D + M + Y_Short,
                D_Num + M_Short + Y,
                D + M_Short + Y,
                D_Num + M_Long + Y,
                D + M_Long + Y,
                Y,
                Y_Short
            ];
            
            Date_Variations.forEach(V => Add_Word(V));
        } else {
            Base_Words.add(DOB_Str);
        }
    }

    if (Keywords_Str) {
        let Keywords = Keywords_Str.split(/\r?\n/);
        Keywords.forEach(K => Add_Word(K.trim()));
    }

    let Base_Array = Array.from(Base_Words);
    
    if (Base_Array.length === 0) {
        document.getElementById("Dict_Status_Text").innerText = "Status : Error - No Inputs Provided";
        document.getElementById("Dict_Status_Text").style.color = "#ff0055";
        return;
    }

    document.getElementById("Generate_Button").disabled = true;
    document.getElementById("Generate_Button").style.opacity = "1";
    document.getElementById("Generate_Button").style.background = "linear-gradient(45deg, #ff8a00, #e52e71)";
    document.getElementById("Generate_Button").style.color = "#fff";
    document.getElementById("Generate_Button").innerText = "Making...";
    
    document.getElementById("Dict_Status_Text").innerText = "Status : Generating Payloads...";
    document.getElementById("Dict_Status_Text").style.color = "#00ffcc";
    
    let T0 = performance.now();
    
    Generated_Lines = [];

    let Final_Combinations = new Set();
    let Separators = ["", " ", "_", "-", "."];
    let Suffixes = ["", "123", "1234", "12345", "12", "1", "!", "@", "!!", "1!", "123!", "2024", "2025", "007", "11"];
    
    for (let Word of Base_Array) {
        for (let Suffix of Suffixes) {
            Final_Combinations.add(Word + Suffix);
            Final_Combinations.add(Suffix + Word);
        }
    }

    let W1_Idx = 0;
    
    function Process_Chunk() {
        let Chunk_End = performance.now() + 16;
        
        while (performance.now() < Chunk_End && W1_Idx < Base_Array.length) {
            let W1 = Base_Array[W1_Idx];
            for (let W2 of Base_Array) {
                if (W1 === W2) continue;
                for (let Sep of Separators) {
                    let Combo = W1 + Sep + W2;
                    for (let Suffix of Suffixes) {
                        Final_Combinations.add(Combo + Suffix);
                    }
                }
            }
            W1_Idx++;
        }
        
        let T_Now = performance.now();
        let Elapsed = (T_Now - T0) / 1000;
        let Count = Final_Combinations.size;
        let Speed = Elapsed > 0 ? Math.floor(Count / Elapsed) : 0;
        
        document.getElementById("Total_Combos").innerText = Count.toLocaleString();
        document.getElementById("Speed_Display").innerText = Speed.toLocaleString();
        
        if (W1_Idx < Base_Array.length) {
            requestAnimationFrame(Process_Chunk);
        } else {
            Generated_Lines = Array.from(Final_Combinations);
            document.getElementById("Dict_Status_Text").innerText = "Status : Generation Complete!";
            document.getElementById("Download_Group").style.display = "flex";
            
            document.getElementById("Generate_Button").disabled = false;
            document.getElementById("Generate_Button").style.background = "transparent";
            document.getElementById("Generate_Button").style.color = "#00ffcc";
            document.getElementById("Generate_Button").innerText = "Generate Dictionary";
        }
    }
    
    requestAnimationFrame(Process_Chunk);
}

function Download_Dictionary() {
    if (Generated_Lines.length === 0) return;
    
    let Content = Generated_Lines.join('\n');
    let Blob_Data = new Blob([Content], { type: "text/plain" });
    let URL_Obj = URL.createObjectURL(Blob_Data);
    
    let Link = document.createElement("a");
    Link.href = URL_Obj;
    Link.download = "Targeted_Dictionary.txt";
    
    document.body.appendChild(Link);
    Link.click();
    document.body.removeChild(Link);
    
    URL.revokeObjectURL(URL_Obj);
}

document.getElementById("Generate_Button").addEventListener("click", Generate_Combinations);
document.getElementById("Download_Button").addEventListener("click", Download_Dictionary);
