import os
import sys
import config

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

    # Check if GPG is enabled and warn if some fields are missing
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
        file.write(f"https://{account['username']}:{account['token']}@{account['host']}")

    print(f"Configuration set for {config_name}.")
