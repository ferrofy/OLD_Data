from decimal import Decimal

def Calculate_Profit(Bp: float, Sp: float, Q: int) -> float:
    return float(round((Decimal(str(Sp)) - Decimal(str(Bp))) * Decimal(str(Q)), 2))

def Distribute_Profit(Profit: float, Savings_List: list) -> list:
    Profit_Paise = int(round(Profit * 100))
    Total_Distributed = 0
    Savings_Index = None

    for I in range(len(Savings_List)):
        if isinstance(Savings_List[I], str):
            continue
            
        if Savings_List[I][0].strip() == "Savings":
            Savings_Index = I
            
        Share = (Profit_Paise * Savings_List[I][2]) // 100
        Savings_List[I][1] = round(Savings_List[I][1] + (Share / 100), 2)
        Total_Distributed += Share
        
    Remaining = Profit_Paise - Total_Distributed
    
    if Savings_Index is not None:
        Savings_List[Savings_Index][1] = round(
            Savings_List[Savings_Index][1] + (Remaining / 100), 2
        )
        
    return Savings_List

def Add_Direct_Amount(Amount: float, Savings_List: list, Category_Name: str) -> list:
    for I in range(len(Savings_List)):
        if isinstance(Savings_List[I], str):
            continue
            
        if Savings_List[I][0].strip() == Category_Name.strip():
            Savings_List[I][1] = round(Savings_List[I][1] + Amount, 2)
            break
            
    return Savings_List