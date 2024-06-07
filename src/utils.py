import os
import sys
import config
import json
import datetime

def check_env(input):
    return os.getenv(input, None)

def check_env_expr(expression):
    if expression.startswith("env:"):
        return os.getenv(expression[4:], None)
    return expression

def readFile(file_path):
    try:
        if file_path.startswith("file:"):
            file_path = file_path[5:]
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

def toLower(input):
    if input is not None:
        return input.lower()
    return None

def doesStartWith(input, start):
    if input is not None:
        return input.startswith(start)
    return False

def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    data = {}
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith(":") and line.endswith(":"):
            current_section = line[1:-1]
            data[current_section] = {}
        elif "=" in line and current_section:
            key, value = line.split("=", 1)
            value = value.strip()
            if value.startswith("{") and value.endswith("}"):
                if value.startswith("{env:"):
                    value = check_env_expr(value[1:-1])
                elif value.startswith("{file:"):
                    value = readFile(value[1:-1])
                else:
                    print(f"Invalid expression: {value}")
            if toLower(value) == "yes":
                value = "true"
            elif toLower(value) == "no":
                value = "false"
            data[current_section][key.strip()] = value

    return data

def get_config_names():
    creds = read_credentials(config.account_dir)
    return list(creds.keys())

def get_account_login(name):
    creds = read_credentials(config.account_dir)
    account = creds[name]
    return f"{account['user.name']} <{account['user.email']}> [{account['username']}]"

def exists(data):
    return data is not None and data != ""

def has_gpg(data):
    return (
        exists(data.get("user.signingkey"))
        or exists(data.get("commit.gpgSign"))
        or exists(data.get("gpg.program"))
    )

def load(config_name):
    creds = read_credentials(config.account_dir)
    account = creds.get(config_name, {})

    if not account:
        print(f"No configuration found for {config_name}.")
        return

    gpg_signing_key = account.get("user.signingkey")
    gpg_program = account.get("gpg.program")
    gpg_sign = account.get("commit.gpgSign")

    if gpg_signing_key or gpg_sign or gpg_program:
        if not gpg_signing_key:
            print(f"Warning: 'user.signingkey' is not set for {config_name}.")
        if not gpg_sign:
            print(f"Warning: 'commit.gpgSign' is not set for {config_name}.")
        if not gpg_program:
            print(f"Warning: 'gpg.program' is not set for {config_name}.")

    print(f"Setting git config for {config_name}...")

    template = f"""[credential]
    helper = store
[user]
    email = {account['user.email']}
    name = {account['user.name']}
{f"    signingkey = {account['user.signingkey']}" if exists(account.get('user.signingkey')) else ""}
[gpg]
    program = {account.get('gpg.program', '/usr/bin/gpg')}
[commit]
    gpgSign = {account.get('commit.gpgSign', 'false')}
    """

    if not exists(account.get("username")):
        print(f"Fatal: 'username' is not set for {config_name}.")
        sys.exit(1)
    if not exists(account.get("token")):
        print(f"Fatal: 'token' is not set for {config_name}.")
        sys.exit(1)

    with open(config.get_git_config_path(), "w") as file:
        file.write(template)

    with open(config.get_git_credentials_path(), "w") as file:
        file.write(f"https://{account['username']}:{account['token']}@github.com")

    print(f"Configuration set for {config_name}.")
    sys.exit(0)

def create():
    config_name = input("Please enter your Configuration Name: ")
    user_name = input("Please enter your Git User Name: ")
    user_email = input("Please enter your Git User Email: ")
    user_signing_key = input("Do you have a GPG Signing Key? (yes/no): ").lower()
    user_token = input("Please enter your GitHub Token: ")
    user_username = input("Please enter your GitHub Username: ")

    use_gpg = False
    gpg_program = ""
    gpg_sign = ""

    if user_signing_key == "yes":
        user_signing_key = input("Please enter your GPG Signing Key: ")
        gpg_program = input("Please enter your GPG Program Path (Leave blank for default '/usr/bin/gpg'): ").strip()
        gpg_sign = input("Do you want to sign your commits with GPG? (yes/no): ").lower()

        if not gpg_program:
            gpg_program = "/usr/bin/gpg"

        use_gpg = True if gpg_sign == "yes" else False

    template = f""":{config_name}:
user.email={user_email}
user.name={user_name}
{f"user.signingkey={user_signing_key}" if use_gpg else ""}
{f"gpg.program={gpg_program}" if use_gpg else ""}
{f"commit.gpgSign={'Yes' if use_gpg else 'No'}" if use_gpg else ""}
username={user_username}
token={user_token}
"""

    try:
        with open(config.account_dir, "a") as file:
            file.write("\n")
            file.write(template)
        print(f"Configuration {config_name} created.")
    except Exception as e:
        print(f"An error occurred: {e}")

def export():
    config_name = input("Please enter the Configuration Name to export (Leave blank to export all): ")
    creds = read_credentials(config.account_dir)
    format = input("Please enter the format to export (json/txt): ").lower()

    export_dir = input("Please enter the export directory (Leave blank for default './exports'): ")
    
    if not export_dir:
        export_dir = "exports"

    if not os.path.exists(export_dir):
            os.mkdir(export_dir)

   
    

    if config_name:
        if format == "json":
            with open(f"{export_dir}/{config_name}.json", "w") as file:
                file.write(json.dumps(creds[config_name]))
        elif format == "txt":
            data = creds[config_name]
            with open(f"{export_dir}/{config_name}.txt", "w") as file:
                file.write(f":{config_name}:\n")
                file.write(f"dataExportedOn={datetime.datetime.now().isoformat()}\n\n")
                for key in data:
                    file.write(f"{key}={data[key]}\n")
        else:
            print("Invalid format.")
            sys.exit(1)
    else:
        if format == "json":
            with open("{export_dir}/all.json", "w") as file:
                file.write(json.dumps(creds))
        elif format == "txt":
            for key in creds:
                data = creds[key]
                with open(f"{export_dir}/{key}.txt", "w") as file:
                    file.write(f":{key}:\n")
                    file.write(f"dataExportedOn={datetime.datetime.now().isoformat()}\n\n")
                    for key in data:
                        file.write(f"{key}={data[key]}\n")
        else:
            print("Invalid format.")
            sys.exit(1)
        
    print("Exported successfully.")


        
