import json
from datetime import date
from pathlib import Path

Base_Dir     = Path(__file__).resolve().parent.parent
Data_Folder  = Base_Dir / "Files" / "Data"
Money_File   = Data_Folder / "Money.py"
History_File = Data_Folder / "History.json"
Goals_File   = Data_Folder / "Goals.json"

class Data_Manager:

    def __init__(Self):
        Self.Savings = []
        Self.Gaps    = []
        Self.History = {}
        Self.Goals   = {"Goal": None, "Alert": None}
        Self.Load_Savings()
        Self.Load_History()
        Self.Save_History()
        Self.Load_Goals()

    def Load_Savings(Self):
        Self.Savings = []
        Self.Gaps    = []
        if not Money_File.exists():
            Self.Savings = [
                ["Invest       ", 0.0, 1],
                ["Savings      ", 0.0, 99],
            ]
            Self.Save_Savings()
            return

        with open(Money_File, "r") as File:
            Content = File.read()
            Lines   = Content.splitlines()
            Item_Index = -1
            In_List    = False
            for Line in Lines:
                Stripped = Line.strip()
                if "Savings = [" in Stripped:
                    In_List = True
                    continue
                if In_List:
                    if Stripped == "]":
                        break
                    if Stripped.startswith("[") or Stripped.startswith('"') or Stripped.startswith("'"):
                        Item_Index += 1
                    elif Stripped == "" and Item_Index >= 0:
                        if Item_Index not in Self.Gaps:
                            Self.Gaps.append(Item_Index)

            Start_Idx = Content.find("Savings = [")
            if Start_Idx != -1:
                Local_Env = {}
                try:
                    exec(Content, {}, Local_Env)
                    Self.Savings = Local_Env.get("Savings", [])
                except Exception:
                    pass

    def Save_Savings(Self):
        Self.Save_History()
        try:
            with open(Money_File, "w") as File:
                File.write("Savings = [\n\n")
                Line = 0
                for Item in Self.Savings:
                    if isinstance(Item, str):
                        File.write(f"\"{Item}\",\n")
                    else:
                        Formatted_Name = f"\"{Item[0]}\""
                        File.write(f"[{Formatted_Name}, {Item[1]}, {Item[2]}],\n")
                    if Line in Self.Gaps:
                        File.write("\n")
                    Line += 1
                File.write("\n]")
            return True
        except Exception:
            return False

    def _Normalize_Entry(Self, V):
        if isinstance(V, dict):
            return V
        return {"b": float(V), "p": 0.0}

    def Load_History(Self):
        Self.History = {}
        if History_File.exists():
            try:
                with open(History_File, "r") as File:
                    Raw = json.load(File)
                for K, V in Raw.items():
                    Self.History[K] = Self._Normalize_Entry(V)
            except Exception:
                pass

    def Save_History(Self):
        Today       = date.today().strftime("%d %b %y")
        Current_Bal = Self.Get_Total_Balance()

        Other_Keys  = [K for K in Self.History if K != Today]
        Prev_Bal    = 0.0
        if Other_Keys:
            Prev_Entry  = Self.History[Other_Keys[-1]]
            Prev_Bal    = Self._Normalize_Entry(Prev_Entry).get("b", 0.0)

        Daily_Profit = round(Current_Bal - Prev_Bal, 2)

        Self.History[Today] = {"b": round(Current_Bal, 2), "p": Daily_Profit}

        try:
            Data_Folder.mkdir(parents=True, exist_ok=True)
            with open(History_File, "w") as File:
                json.dump(Self.History, File, indent=4)
        except Exception:
            pass

    def Load_Goals(Self):
        Self.Goals = {"Goal": None, "Alert": None}
        if Goals_File.exists():
            try:
                with open(Goals_File, "r") as File:
                    Self.Goals = json.load(File)
            except Exception:
                pass

    def Save_Goals(Self):
        try:
            Data_Folder.mkdir(parents=True, exist_ok=True)
            with open(Goals_File, "w") as File:
                json.dump(Self.Goals, File, indent=4)
            return True
        except Exception:
            return False

    def Get_Total_Balance(Self):
        Bal = sum(round(Item[1], 2) for Item in Self.Savings if isinstance(Item, list))
        return round(Bal, 2)

    def Get_Balances_Dict(Self):
        return {Item[0].strip(): Item[1] for Item in Self.Savings if isinstance(Item, list)}

    def Get_Hist_Balances(Self):
        return [Self._Normalize_Entry(V).get("b", 0.0) for V in Self.History.values()]

    def Get_Hist_Profits(Self):
        return [Self._Normalize_Entry(V).get("p", 0.0) for V in Self.History.values()]
