### Codyssey Mars project2 ### 
### Edit by Mariner_정찬수 ###

from typing import List, Tuple
import csv
import pickle

CSV_FILE = './mars_base/Mars_Base_Inventory_List.csv'

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def print_csv_file_and_out_list() -> list:
    csv_list :List[Tuple[str, str, str, str, str]] = []

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        buf = f.readline()
        if not buf:
            raise Exception('File is empty!')

        header = buf.strip('\n').split(',')
        if (
            len(header) < 5
            or header[0] != "Substance"
            or header[1] != "Weight (g/cm³)"
            or header[2] != "Specific Gravity"
            or header[3] != "Strength"
            or header[4] != "Flammability"
        ):
            raise ValueError("Invalid csv format!")

        while True:
            # print row file by line
            print(buf, end='')
            buf = f.readline()
            if not buf:
                break
            tokens = buf.strip('\n').split(',')

            # Formatting to 3 decimal places
            tks = []
            for tok in tokens:
                dot_idx = tok.find('.')
                if is_number(tok):
                    tks.append(tok[:dot_idx + 4]) # python slicing
                else:
                    tks.append(tok)

            csv_list.append((tks[0], tks[1], tks[2], tks[3], tks[4]))
        
    return csv_list

def save_csv_file(csv_list: list, CSV_FILE='./Mars_Base_Inventory_danger.csv'):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_list)

### bonus ### -> C와 호환되게 만드는 법 (정신건강에 나쁘다.)
#import struct

# def save_binary_file(csv_list: list, CSV_FILE='./Mars_Base_Inventory_List.bin'):
#     with open(CSV_FILE, 'wb') as f:
#         for row in csv_list:
#             encoded_row: list = []
#             for col in row:
#                 encoded_row.append(str(col).encode('utf-8')[:10])
#             f.write(struct.pack('10s10s10s10s10s', *encoded_row))

### bonus ###
def save_binary_file(csv_list: list, CSV_FILE='./Mars_Base_Inventory_List.bin'):
    with open(CSV_FILE, 'wb') as f:
        pickle.dump(csv_list, f)

def read_binary_file(BIN_FILE='./Mars_Base_Inventory_List.bin'):
    with open(BIN_FILE, 'rb') as f:
        data = pickle.load(f)
        print("\n--- READ BINARY FILE ---")
        for row in data:
            print(row)

def main():
    try:
        csv_list = print_csv_file_and_out_list()
        sorted_list = sorted(csv_list, key=lambda x: x[4], reverse=True)
        filtered_list = [row for row in sorted_list if float(row[4]) > 0.7]
        save_csv_file(filtered_list)
        print('--- Sorted by Flammability and over 0.7---')
        for row in filtered_list:
            print(row)

        ##bonus##
        save_binary_file(sorted_list)
        read_binary_file()

    except FileExistsError:
        print('File not found!')
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()