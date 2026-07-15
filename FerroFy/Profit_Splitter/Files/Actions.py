from Files import Calculations

def Resell_Action(Dm, Category_Index: int, Bp: float, Sp: float, Q: int) -> None:
    Profit = Calculations.Calculate_Profit(Bp, Sp, Q)
    Dm.Savings = Calculations.Distribute_Profit(Profit, Dm.Savings)
    Principal = round(Bp * Q, 2)
    
    if 0 <= Category_Index < len(Dm.Savings) and isinstance(Dm.Savings[Category_Index], list):
        Cat_Name = Dm.Savings[Category_Index][0]
    else:
        Cat_Name = next(Item[0] for Item in Dm.Savings if isinstance(Item, list))
        
    Dm.Savings = Calculations.Add_Direct_Amount(Principal, Dm.Savings, Cat_Name)

def Rewards_Action(Dm, Amount: float) -> None:
    Dm.Savings = Calculations.Distribute_Profit(Amount, Dm.Savings)

def Loan_Action(Dm, Amount: float) -> None:
    Percentage = 95
    Reinvest = round(Amount * (Percentage / 100), 2)
    To_Distribute = round(Amount * ((100 - Percentage) / 100), 2)
    
    Shop_Categories = []
    In_Shop = False
    for Item in Dm.Savings:
        if isinstance(Item, str):
            In_Shop = (Item.strip() == "Shop")
        elif In_Shop and isinstance(Item, list):
            Shop_Categories.append(Item[0].strip())
            
    if Shop_Categories:
        Equal_Share = round(Reinvest / len(Shop_Categories), 2)
        Total_Shared = Equal_Share * len(Shop_Categories)
        Diff = round(Reinvest - Total_Shared, 2)
        
        for I, Cat_Name in enumerate(Shop_Categories):
            Amount_To_Add = Equal_Share
            if I == 0:
                Amount_To_Add = round(Amount_To_Add + Diff, 2)
            Dm.Savings = Calculations.Add_Direct_Amount(Amount_To_Add, Dm.Savings, Cat_Name)
            
    Dm.Savings = Calculations.Distribute_Profit(To_Distribute, Dm.Savings)

def Transfer_Action(Dm, From_Index: int, To_Index: int, Amount: float) -> None:
    if 0 <= From_Index < len(Dm.Savings) and 0 <= To_Index < len(Dm.Savings):
        if isinstance(Dm.Savings[From_Index], list) and isinstance(Dm.Savings[To_Index], list):
            Cat_1 = Dm.Savings[From_Index][0]
            Cat_2 = Dm.Savings[To_Index][0]
            Dm.Savings = Calculations.Add_Direct_Amount(-Amount, Dm.Savings, Cat_1)
            Dm.Savings = Calculations.Add_Direct_Amount(Amount, Dm.Savings, Cat_2)

def Spend_Action(Dm, Category_Index: int, Amount: float) -> None:
    if 0 <= Category_Index < len(Dm.Savings):
        if isinstance(Dm.Savings[Category_Index], list):
            Cat = Dm.Savings[Category_Index][0]
            Dm.Savings = Calculations.Add_Direct_Amount(-Amount, Dm.Savings, Cat)