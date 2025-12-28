import pandas as pd
import os
import random2 as rd

const = [0, 1, 3, 4, 6]

# ---------------- TIME TABLE CLASS ---------------- #
class TimeTable:
    def __init__(self, file_path="teachers.xlsx"):
        self.columns = ['Name', 'Total_Hours', 'Subject', 'Sub_Code']
        self.file_path = file_path

        # -------- TIME TABLE -------- #
        self.DT = pd.DataFrame(
            columns=[f"Day{i}" for i in range(1, 7)],
            index=range(10)
        )

        # Break / Lunch
        self._set_breaks()

        # -------- LOAD DATA -------- #
        self.df = self._load_existing()
        

        

    # ---------------- INITIALIZATION OF BREAKS/LUNCH ---------------- #
    def _set_breaks(self):
        self.DT.loc[2, :] = "Break"
        self.DT.loc[5, :] = "Lunch"
        self.DT.loc[8, :] = "Break"

    # ---------------- TIME TABLE GENERATOR ---------------- #
    def time_table(self):
        lab_day = []
        i = 0

        while i < len(self.df):
            hour = int(self.df.loc[i, 'Total_Hours'])
            subj = self.df.loc[i, "Subject"]

            # -------- LAB SUBJECT -------- #
            if "lab" in subj.lower():
                attempts = 0
                placed = False

                while attempts < 200 and not placed:
                    attempts += 1
                    period = rd.choice(const)
                    day = rd.randint(1, 6)

                    rows = [period + x for x in range(hour)]
                    rows = self.update_rows(rows)

                    if not rows:
                        continue
                    if day in lab_day:
                        continue

                    col = self.DT.loc[rows, f"Day{day}"]
                    if col.isna().all():
                        self.DT.loc[rows, f"Day{day}"] = subj
                        lab_day.append(day)
                        placed = True

                i += 1
                continue

            # -------- THEORY SUBJECT -------- #
            try_ = 0
            j = 0
            while j < hour and try_ < 200:
                row = rd.randint(0, 9)
                day = rd.randint(1, 6)
                try_ += 1

                if self.DT.loc[row, f"Day{day}"] in ["Break", "Lunch"]:
                    continue
                if not pd.isna(self.DT.loc[row, f"Day{day}"]):
                    continue

                self.DT.loc[row, f"Day{day}"] = subj
                j += 1

            i += 1

        
      
  

    # ---------------- RESET (FULL RESET) ---------------- #
    def reset(self):

        # -------- RESET TIME TABLE -------- #
        self.DT = pd.DataFrame(
            columns=[f"Day{i}" for i in range(1, 7)],
            index=range(10)
        )
        self._set_breaks()

        # -------- RESET DATAFRAME -------- #
        self.df = pd.DataFrame(columns=self.columns)

        # -------- CLEAR EXCEL FILE -------- #
        self.df.to_excel(
            self.file_path,
            index=False,
            engine="openpyxl"
        )

        # -------- RESET DISPLAY -------- #
        self.table = "No records."
        self.Tt = ""

        print("All data reset successfully.")

    # ---------------- ROW UPDATION ---------------- #
    def update_rows(self, rows):
        updated = []

        for r in rows:
            if r in [2, 5, 8]:
                r += 1

            if r > 9:
                return []

            while r in updated or r in [2, 5, 8]:
                r += 1
                if r > 9:
                    return []

            updated.append(r)

        return sorted(updated)

    # ---------------- LOAD DATA ---------------- #
    def _load_existing(self):
        if os.path.exists(self.file_path):
            try:
                existing = pd.read_excel(
                    self.file_path,
                    sheet_name=0,
                    engine="openpyxl"
                )
                for c in self.columns:
                    if c not in existing.columns:
                        existing[c] = pd.NA
                return existing[self.columns].reset_index(drop=True)
            except Exception:
                return pd.DataFrame(columns=self.columns)
        return pd.DataFrame(columns=self.columns)



    # ---------------- SAVE ---------------- #
    def save(self):
        try:
            self.df.to_excel(
                self.file_path,
                index=False,
                sheet_name="Sheet1",
                engine="openpyxl"
            )
            print(f"Saved data to {self.file_path}")
        except Exception as e:
            print("Error saving file:", e)

    # ---------------- ADD DATA ---------------- #
    def get_data(self, name, sub_hd, TH, sub_code):
        new_row = {
            'Name': name,
            'Total_Hours': TH,
            'Subject': sub_hd,
            'Sub_Code': sub_code
        }
        self.df = pd.concat(
            [self.df, pd.DataFrame([new_row])],
            ignore_index=True
        )
       
        self.save()

    # ---------------- UPDATE DATA ---------------- #
    def update_data(self):
        if self.df.empty:
            print("No data to update.")
            return

        print(self.table)
        try:
            idx = int(input("Index to update: "))
        except ValueError:
            return

        if idx not in range(len(self.df)):
            print("Invalid index.")
            return

        print("1.Name  2.Total Hours  3.Subject  4.Subject Code")
        ch = int(input("Choice: "))

        if ch == 1:
            self.df.at[idx, 'Name'] = input("New name: ")
        elif ch == 2:
            self.df.at[idx, 'Total_Hours'] = int(input("New hours: "))
        elif ch == 3:
            self.df.at[idx, 'Subject'] = input("New subject: ")
        elif ch == 4:
            self.df.at[idx, 'Sub_Code'] = input("New code: ")

        
        self.save()

    # ---------------- DELETE ---------------- #
    def delete(self, index):
        if 0 <= index < len(self.df):
            self.df.drop(index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
           
            self.save()
        else:
            return "<h1>Invalid Choice.....</h1>"


# ---------------- MAIN ---------------- #
if __name__ == "__main__":

    pass