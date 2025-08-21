

LOG_FILE = mission_computer_main.log

def main():
	print_log_file()

	log_list = log_to_list()

	print(log_list)

	print(sorted(log_list, key=lambda x: x[0], reverse=True))

	log_dict = list_to_dict(log_list)

	save_json_file(log_dict)

if __name__ == "__main__":
	main()
