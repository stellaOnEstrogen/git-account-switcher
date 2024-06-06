import os
import utils

account_dir = utils.check_env('ACCOUNT_DIR') or os.path.join("data", "accounts.creds")

user_profile = os.getenv('USERPROFILE', 'C:\\Users\\Default')
home_dir = os.getenv('HOME', '/home/default')

git_config_paths = {
    'nt': os.path.join(user_profile, ".gitconfig"),
    'posix': os.path.join(home_dir, ".gitconfig"),
    'darwin': os.path.join(home_dir, ".gitconfig")
}

git_credentials_paths = {
    'nt': os.path.join(user_profile, ".git-credentials"),
    'posix': os.path.join(home_dir, ".git-credentials"),
    'darwin': os.path.join(home_dir, ".git-credentials")
}

def get_git_config_path():
    return git_config_paths.get(os.name, home_dir)

def get_git_credentials_path():
    return git_credentials_paths.get(os.name, home_dir)
