from prettytable import PrettyTable
import praw
import sys
import getpass

r = praw.Reddit(user_agent="I'm a b0t motherfucker!")
login = False

while login == False:
    username = str(input('Username: '))

    if sys.stdin.isatty():
        password = getpass.getpass()
    else:
        password = str(input('Password: '))

    try:
        r.login(username, password, disable_warning=True)
        login = True
    except praw.errors.InvalidUserPass:
        print('Invalid Username or Password')

limit = int(input('How many saved posts do you want to retrieve (Default is all): ')) or None

saved = list(r.user.get_saved(limit=limit))
saved_subs = {}
saved_type = {'Link': 0, 'Text': 0}

for post in saved:
    url = post.permalink
    start = url.find('/r/') + len('/r/')
    end = url.find("/comments/")
    subreddit = url[start:end]

    if subreddit in saved_subs:
        saved_subs[subreddit] += 1
    else:
        saved_subs[subreddit] = 1

    if type(post) == praw.objects.Submission:
        saved_type['Link'] += 1
    else:
        saved_type['Text'] += 1



sub_table = PrettyTable(['Subreddit', 'Saved Posts'])
type_table = PrettyTable(['Type', 'Saves'])

for key, value in saved_subs.items():
    sub_table.add_row([key, value])

for key, value in saved_type.items():
    type_table.add_row([key, value])

print(sub_table.get_string(sortby="Saved Posts", reversesort=True))
print(type_table.get_string(sortby="Type", reversesort=False))