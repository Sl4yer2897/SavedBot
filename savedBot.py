from prettytable import PrettyTable
import praw
import sys
import getpass

r = praw.Reddit(user_agent="I'm a b0t motherfucker!")
login = False

# Loops continuously until a successful login
while login == False:
    # Username Input
    username = str(input('Username: '))

    # Password input
    # If script is executed in a TTY, the password is read using "getpass" which suppresses the echo of the password
    # to stdout (i.e. hides it from the screen.) Some IDEs don't use a TTY to run code, so this will default to input().
    if sys.stdin.isatty():
        password = getpass.getpass()
    else:
        password = str(input('Password: '))


    # Attempt login
    try:
        r.login(username, password, disable_warning=True)
        login = True

    # Catches errors thrown by an invalid username or password
    except praw.errors.InvalidUserPass:
        print('Invalid Username or Password')

# Queries the user on how many posts to retrieve
limit = int(input('How many saved posts do you want to retrieve (Default is all): ')) or None

# Retrieves number of posts requested by the user and inserts them into a list
saved = list(r.user.get_saved(limit=limit))

# Creates dictionaries to be used with "PrettyTables"
saved_subs = {}
saved_type = {'Link': 0, 'Text': 0}

# Loops through the list (var = saved) of saved posts
for post in saved:
    # Gets the url of the post and saves it to a variable
    url = post.permalink

    # Searches for '/r/' in the url (which will be right before the subreddit name)
    start = url.find('/r/') + len('/r/')

     # Searches for '/comments/' in the url (which will be right after the subreddit name)
    end = url.find("/comments/")

    # Gets the text between '/r/' and '/comments/' (i.e. the subreddit name.)
    subreddit = url[start:end]

    # If the subreddit name is already a key in the dictionary, increment its value by 1
    if subreddit in saved_subs:
        saved_subs[subreddit] += 1

    # If the subreddit name is NOT already a key in the dictionary, add it as a key and set its value to 1
    else:
        saved_subs[subreddit] = 1

    # If the post is a link, increment the link counter by 1
    if type(post) == praw.objects.Submission:
        saved_type['Link'] += 1

    # If the post is a comment, increment the comment counter by 1
    else:
        saved_type['Text'] += 1


# Create the ASCII tables with "PrettyTables"
sub_table = PrettyTable(['Subreddit', 'Saved Posts'])
type_table = PrettyTable(['Type', 'Saves'])

# Loop through each subreddit name and post count, and add the values to an ASCII table for printing
for key, value in saved_subs.items():
    sub_table.add_row([key, value])

# Loop through each post type and type count, and add the values to an ASCII table for printing
for key, value in saved_type.items():
    type_table.add_row([key, value])

# Print the ASCII tables
print(sub_table.get_string(sortby="Saved Posts", reversesort=True))
print(type_table.get_string(sortby="Type", reversesort=False))