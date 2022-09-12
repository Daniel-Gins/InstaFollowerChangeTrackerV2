import os
import sys
from instagrapi import Client
from pwinput import pwinput
from tempfile import gettempdir
from datetime import datetime
from pathlib import Path

# Get user information
username = input("Username: ").strip()
password = pwinput()
oauth = input("2FA Code (if not exists, leave blank): ").strip()
print()

# Account settings dump path
DUMP = os.path.join(gettempdir(), "{}_account_dump.json".format(username))
BACKUP = os.path.join(str(Path.home()), "{}_follower_dump.instabackup".format(username))

# Try to login and get account details, if fails, terminate
try:
    # Create the client
    cl = Client()

    # If there is a dump for the account, load settings
    if os.path.exists(DUMP):
        cl.load_settings(DUMP)
        print("Loaded account settings from dump.")

    # Login
    cl.login(username, password, verification_code=oauth)

    # If there is not a dump for the account, dump settings
    if not os.path.exists(DUMP):
        cl.dump_settings(DUMP)
        print("Dumped account settings to temp directory.")
    
    # Get the user ID
    user_id = cl.user_id
    print("Your User ID: {}".format(user_id))

    # Get followers
    print("Getting accounts that follow you...")
    followers = cl.user_followers(user_id)
    print("Got {} followers.".format(len(followers)))
except Exception as e:
    # Print the exception message
    print("An exception occured: {}".format(str(e)))

    # Delete account dump to prevent login issues
    if os.path.exists(DUMP):
        os.remove(DUMP)
        print("Account dump is deleted to prevent login issues.")

    # Terminate
    input("Press Enter to terminate.")
    sys.exit(1)

# Extract only the usernames on both followed accounts and followers
followers_dict = {}

for i in followers.values():
    followers_dict[i.pk] = i.username

# If there is no backup, create the backup and terminate
if not os.path.exists(BACKUP):
    print("Backup not found. Creating a new backup...")

    # Create the backup file
    with open(BACKUP, "w") as file:
        file.write(str(datetime.now()) + "\n" + "\n".join([";".join(i) for i in followers_dict.items()]))
    
    # Terminate
    input("Press Enter to terminate.")
    sys.exit(0)

# Get backup values
print("Getting backup...")
with open(BACKUP, "r") as file:
    lines = file.readlines()
timestamp = lines.pop(0).strip()
old_backup = {}
for i in lines:
    item = i.strip().split(";")
    old_backup[item[0]] = item[1]

print("Latest backup timestamp: " + timestamp) # Print the backup timestamp

# Follower change lists
new_followers = []
unfollowed = []

# Get new followers
for i in followers_dict.items():
    if i[0] not in old_backup.keys():
        new_followers.append(i[1])

# Get users who have unfollowed
for i in old_backup.items():
    if i[0] not in followers_dict.keys():
        unfollowed.append(i[1])

print()
# If there are no changes, terminate
if len(new_followers) == 0 and len(unfollowed) == 0:
    print("No new changes on followers. Nothing is saved.")
    input("Press Enter to terminate.")
    sys.exit(0)

# Get the path for results
path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', "{}_follower_changes.html".format(username))

# Print the new followers and fill an HTML body with them and their Instagram profiles
html = "<b>Timestamp:</b> {}<br><br>".format(str(datetime.now()))
if len(new_followers) != 0:
    print("New followers:")
    print("\n".join(new_followers))

    html += "<b>New followers:</b><br>"
    for i in new_followers:
        html += '<a href="https://instagram.com/{}">{}</a><br>'.format(i, i)

    if len(unfollowed) != 0:
        print()
        html += "<br>"

# Print the unfollowed users and fill an HTML body with them and their Instagram profiles
if len(unfollowed) != 0:
    print("Unfollowed:")
    print("\n".join(unfollowed))

    html += "<b>Unfollowed:</b><br>"
    for i in unfollowed:
        html += '<a href="https://instagram.com/{}">{}</a><br>'.format(i, i)

# Open the file and write the results into it
with open(path, "w") as file:
    file.write(html)

# Backup again
with open(BACKUP, "w") as file:
    file.write(str(datetime.now()) + "\n" + "\n".join([";".join(i) for i in followers_dict.items()]))

# Print the path and terminate
print("\nResults are saved to {}.".format(path))
input("Press Enter to terminate.")