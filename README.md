# InstaFollowerChangeTracker
Keep track of new followers and users who have unfollowed.

## Dependencies
* Python >= 3.7, recommend 3.8+
* Instagrapi
* PWInput
* Pillow

## Usage
First, install the required modules (check requirements.txt).

#### Installation
Dependencies can be installed via the following command:
```
pip install -r requirements.txt
```

After the installation process, you have to run the script enter your Instagram credentials to get new followers and users who have unfollowed.* On the first run, the script will create a backup file. Every run after the first one, it will compare the current followers with the backup and overwrite the previous backup. The results are printed and saved to a file on your desktop.

Please note that this script only checks the usernames, so if there is a username change, it will identify it as both unfollow and follow. It also does not handle deleted accounts. To get an accurate result, please double-check the outputted accounts.

*NOTE: If you receive an email about a login attempt from an unrecognized device (for example Xiaomi Mi 5s), do not panic. The user agent that Instagrapi provides is different than your device. Also, do not run the script back to back. Instagram may see it as suspicious activity and temporarily lock your account. In some cases, Instagram gives a warning about a suspicious login on the app and blocks the script access. If this is the case, after running the script, immediately press "This was me".

PS. To login, either Two-Factor-Authentication via auth app has to be enabled or 2FA has to be disabled.
