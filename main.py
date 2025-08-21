### Codyssey Mars project ### 
### Edit by Mariner_정찬수 ###

from typing import List, Tuple
import json

LOG_FILE = 'mission_computer_main.log'


def print_log_file_and_out_list() -> list:
    log_list :List[Tuple[str, str]] = []

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        buf = f.readline()
        if not buf:
            raise Exception('File is empty!')

        tokens = buf.strip('\n').split(',')
        if len(tokens) < 3 or tokens[0] != 'timestamp' or tokens[1] != 'event' or tokens[2] != 'message':
            raise ValueError('Invalid log format!') 
        
        while True:
            print(buf, end='')
            buf = f.readline()
            if not buf:
                break
            tokens = buf.strip('\n').split(',')
            log_list.append((tokens[0], tokens[2]))
        
    return log_list

def save_json_file(log_dict: dict, JSON_FILE='./mission_computer_main.json') -> None:
	with open(JSON_FILE, 'w', encoding='utf-8') as f:
		json.dump(log_dict, f, ensure_ascii=False, indent=4)

def main():
    try:
        log_list = print_log_file_and_out_list()
        sorted_list = sorted(log_list, key=lambda x: x[0], reverse=True)
        log_dict = dict(sorted_list)
        save_json_file(log_dict)

        print('--- log_list ---')
        for log in log_list:
            print(log)

        print('--- Reverse ---')
        for log in sorted_list:
            print(log)

    except FileExistsError:
        print('File not found!')
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
