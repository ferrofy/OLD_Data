import time

def Loading_Bar(Width_Of_Bar, Speed , Inner_Bar = "█"):

    Start_Time = time.time()

    for i in range(Width_Of_Bar + 1):
        Bar = f"{Inner_Bar}" * i
        Space = " " * (Width_Of_Bar - i)
        Percent = int((i / Width_Of_Bar) * 100)
        Elapsed_Time = time.time() - Start_Time

        if i > 0:
            Estimated_Total = (Elapsed_Time / i) * Width_Of_Bar
            Remaining_Time = Estimated_Total - Elapsed_Time
        else:
            Remaining_Time = 0

        print(
            f"\r[{Bar}{Space}] {Percent}% | Estimated Remaining: {Remaining_Time:.2f}s",
            end="",
            flush=True
        )

        time.sleep(Speed)

    Total_Time = time.time() - Start_Time

    print(f"\nCompleted In {Total_Time:.2f} Seconds ✅")


Loading_Bar(120, 0.01 )