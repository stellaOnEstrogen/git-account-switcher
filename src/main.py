import sys
import time
import utils

def get_index_of_config(configs, config_name):
    for i, config in enumerate(configs):
        if config == config_name:
            return i + 1
    return -1

def toInt(input):
    try:
        return int(input)
    except ValueError:
        return -1

def index_to_config_name(configs, index):
    return configs[index - 1]

def main():
    configs = utils.get_config_names()

    print("Welcome to the Git Account Manager!")
    print("Developed by: @haydenHighOnLife")
    print("Available configurations:")
    for _config in configs:
        data = utils.get_account_login(index_to_config_name(configs, get_index_of_config(configs, _config)))
        print(f"  - {_config} ({get_index_of_config(configs, _config)}) {data}")
    print("Please select a configuration to use (by index // Example: 1):")

    config_name_index = input()
    config_name = index_to_config_name(configs, int(config_name_index))

    if config_name not in configs:
        print("Invalid configuration name.")
        sys.exit(1)

    print(f"Using configuration: {config_name}")
    time.sleep(2)
    
    utils.load(config_name=config_name)

if __name__ == '__main__':
    main()
