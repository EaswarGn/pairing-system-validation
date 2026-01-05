import os
import json
from convert import build_sections_from_JSON

def check_and_rename_files():
    tournaments = ['t1','t2','t3','t4','t5']
    for tournament in tournaments:
        for file in os.listdir(f"solutions/{tournament}"):

            if file.endswith(".json") and os.path.exists(f"solutions/{tournament}/{file}"):
                with open(f"solutions/{tournament}/{file}") as f:
                    JSON = json.loads(f.read())

                sec1 = build_sections_from_JSON(JSON)
                parts = file.split('_')
                t_index = parts[0]
                s_index = parts[1]
                r_index = parts[2].split('.')[0]  # remove ".json" from r#

                print("Checking section: " + file)
                l = sec1[0].checkTopVsBottomHalf(int(r_index[1:]))

                if len(l) > 10:
                    t = sec1[0].checkTopVsBottomHalfTest(int(r_index[1:]))
                    print(t, len(t))
                    print(len(sec1[0].players))
                    # If it does, rename this file and all other matching t#_s#_ files
                    if  input("Move file? (y/n): ") == "y":
                        for file_to_rename in os.listdir(f"solutions/{tournament}"):
                            if file_to_rename.startswith(f"{t_index}_{s_index}_"):
                                os.replace(f"solutions/{tournament}/{file_to_rename}", f"solutions/accel/{file_to_rename}")
                                os.replace("inputs/{}/{}".format(tournament, file_to_rename.replace("_solution", "")), "inputs/accel/{}".format(file_to_rename.replace("_solution", "")))

# Usage
check_and_rename_files()
