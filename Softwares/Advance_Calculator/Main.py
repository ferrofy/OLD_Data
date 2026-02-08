import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

from FerroFy import Exit
from FerroFy import Entry

Entry.Main_Logo()

Action = input("""
        --------|  Basic  |--------
                   
[0] ---> Addition / Subtraction
[1] ---> Multiplication
[2] ---> Division
[3] ---> Average
                   
        --------|  Advanced  |--------
                   
[000] ---> Determinant Of Matrix
[001] ---> Attendence Calculator
[002] ---> CGPA Calculator
[003] --->  { Comming Soon }
[003] ---> 
[004] --->

What Operation You Want To Preform ----> """).strip()


if Action == "0":
    from Files import Addition
    Addition.Add()

elif Action == "1":
    from Files import Multiplication
    Multiplication.Multiply()

elif Action == "2":
    from Files import Division
    Division.Divide()

elif Action == "3":
    from Files import Average
    Average.Avg()

elif Action == "000":
    from Files import Determinant
    Determinant.Det()

elif Action == "001":
    from Files import Attendence_Calculator
    Attendence_Calculator.Calculate()

elif Action == "002":
    from Files import CGPA_Calculator
    CGPA_Calculator.Calculate()

else:
    print("Wrong Input...")

Exit.Calculator()