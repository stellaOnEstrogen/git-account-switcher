# Creating the Credentials File


## Overview

To effectively utilize this program, you'll need to set up a credentials file. This file will store crucial information necessary for seamlessly switching between various accounts.

The credentials file follows a specific format, outlined below:

```
:My First Account: 
user.email=YOUR_EMAIL
user.name=YOUR_NAME
user.signingkey=YOUR_SIGNING_KEY
gpg.program=PATH_TO_GPG_PROGRAM
commit.gpgSign=Yes_or_No
username=YOUR_GITHUB_USERNAME
token=YOUR_GITHUB_TOKEN
```


You can add multiple accounts within this file, each delineated by a section enclosed in colons (`:`).

- **`:My First Account:`**: This is the customizable name of your account. While you can name it as you wish, ensure it's encapsulated within colons.

- **`user.email`, `user.name`, `user.signingkey`, `gpg.program`, `commit.gpgSign`, `username`, and `token`**: These are the essential fields you'll fill for each account, providing details such as email, name, signing key, GPG program path, commit GPG sign preference, GitHub username, and token.

## Functions

Functions within the credentials file allow dynamic handling of data, such as retrieving environment variables or reading from files.

### `env:`

The `env:` function fetches environment variables from your system.

```plaintext
(...)
token={env:GITHUB_TOKEN}
(...)
```

### `file:`

The `file`: function reads content from a specified file.

```
(...)
token={file:./path/to/file}
(...)
```

Certainly! Here's the improved documentation wrapped in a single code block:

plaintext

# Creating the Credentials File

## Overview
To effectively utilize this program, you'll need to set up a credentials file. This file will store crucial information necessary for seamlessly switching between various accounts.

The credentials file follows a specific format, outlined below:

```
:First Account:

user.email=YOUR_EMAIL
user.name=YOUR_NAME
user.signingkey=YOUR_SIGNING_KEY
gpg.program=PATH_TO_GPG_PROGRAM
commit.gpgSign=Yes_or_No
username=YOUR_GITHUB_USERNAME
token=YOUR_GITHUB_TOKEN

```


You can add multiple accounts within this file, each delineated by a section enclosed in colons (`:`).

- **`:My First Account:`**: This is the customizable name of your account. While you can name it as you wish, ensure it's encapsulated within colons.

- **`user.email`, `user.name`, `user.signingkey`, `gpg.program`, `commit.gpgSign`, `username`, and `token`**: These are the essential fields you'll fill for each account, providing details such as email, name, signing key, GPG program path, commit GPG sign preference, GitHub username, and token.

## Functions

Functions within the credentials file allow dynamic handling of data, such as retrieving environment variables or reading from files.

### `env:`

The `env:` function fetches environment variables from your system.

```plaintext
(...)
token={env:GITHUB_TOKEN}
(...)

file:

The file: function reads content from a specified file.

plaintext

(...)
token={file:./path/to/file}
(...)

Integrating these functions enhances the flexibility and utility of your credentials setup.