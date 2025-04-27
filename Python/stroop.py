import pandas as pd

data_path = "./data.csv"
replace_Nulls = True
stroop_data_dir = "./experiment_data/"
output_file = "output.csv"

def get_avg_data(filename, col_match):
    avrs_time = []
    avrs_value = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(" ")
            if parts[0] == "training":
                continue
            if col_match and parts[1] != parts[2]:
                continue
            if not col_match and parts[1] == parts[2]:
                continue
            avrs_time.append(int(parts[-1]))
            val = int(parts[-2])
            if val == 3:
                val = 2
            avrs_value.append(val)
    if len(avrs_time) == 0:
        return (0, 0)
    return (sum(avrs_time) / len(avrs_time), sum(avrs_value) / len(avrs_value))


df = pd.read_csv(data_path)


if replace_Nulls:
    df = df.fillna(0)
    df.replace(["", " "], "0", inplace=True)


for col in [7, 16]:
    path_col = df.columns[col]
    new_avg_val_col = "Sredni_Wynik_Testu_{}_Kolory".format(1 if col == 7 else 2)
    new_avg_time_color = "Sredni_Czas_Testu_{}_Kolory".format(1 if col == 7 else 2)
    new_avg_val_name = "Sredni_Wynik_Testu_{}_Nazwy".format(1 if col == 7 else 2)
    new_avg_time_name = "Sredni_Czas_Testu_{}_Nazwy".format(1 if col == 7 else 2)

    avg_val_colors = []
    avg_time_colors = []
    avg_val_names = []
    avg_time_names = []

    for filename in df[path_col]:
        filepath = stroop_data_dir + str(filename)
        avg_time, avg_val = get_avg_data(filepath, True)
        avg_val_colors.append((avg_val - 2) * -1)
        avg_time_colors.append(avg_time)

        avg_time, avg_val = get_avg_data(filepath, False)
        avg_val_names.append((avg_val - 2) * -1)
        avg_time_names.append(avg_time)

    df[path_col] = avg_val_colors
    df.insert(col + 1, new_avg_time_color, avg_time_colors)
    df.insert(col + 2, new_avg_val_name, avg_val_names)
    df.insert(col + 3, new_avg_time_name, avg_time_names)


df.to_csv(output_file, index=False)

    

