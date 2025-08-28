### Codyssey Mars project3 ###
### Edit by Mariner_정찬수 ###

import numpy as np
import csv

PARTS1 = "./mars_base/mars_base_main_parts-001.csv"
PARTS2 = "./mars_base/mars_base_main_parts-002.csv"
PARTS3 = "./mars_base/mars_base_main_parts-003.csv"
OUT_CSV = "./parts_to_work_on.csv"


def main():
    try:
        items = np.genfromtxt(
            PARTS1, dtype=None, delimiter=",", usecols=[0], skip_header=1
        )
        arr1 = np.genfromtxt(
            PARTS1, dtype=None, delimiter=",", usecols=[1], skip_header=1
        )
        arr2 = np.genfromtxt(
            PARTS2, dtype=None, delimiter=",", usecols=[1], skip_header=1
        )
        arr3 = np.genfromtxt(
            PARTS3, dtype=None, delimiter=",", usecols=[1], skip_header=1
        )

        tab = np.column_stack([arr1, arr2, arr3])
        avg = (arr1 + arr2 + arr3) / 3

        dtype = [
            ("items", "U64"),
            ("tab1", int),
            ("tab2", int),
            ("tab3", int),
            ("avg", float),
        ]
        parts = np.empty(
            items.shape[0], dtype=dtype
        )  # items.shape[0] : items 행의 개수

        parts["items"] = items
        parts["tab1"] = tab[:, 0]
        parts["tab2"] = tab[:, 1]
        parts["tab3"] = tab[:, 2]
        parts["avg"] = avg

        mask = parts["avg"] < 50
        filtered = parts[mask]

        header = ["items", "tab1", "tab2", "tab3", "avg"]

        with open(OUT_CSV, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in filtered:
                writer.writerow(
                    [
                        row["items"],
                        row["tab1"],
                        row["tab2"],
                        row["tab3"],
                        f"{row['avg']:.3f}",
                    ]
                )

    except FileExistsError:
        print("File not found!")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
