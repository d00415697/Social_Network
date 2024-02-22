#!/usr/bin/env python3

import click
import os
import sqlite3
import sys

DB_FILE = 'network.db'

def getdb(create=False):
    if os.path.exists(DB_FILE):
        if create:
            os.remove(DB_FILE)
    else:
        if not create:
            print('no database found')
            sys.exit(1)
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con

@click.group()
def cli():
    pass

@click.command()
def create():
    print("Welcome to Face, a state-of-the-art social network.")
    print("Creating database.")
    with getdb(create=True) as con:
        con.execute(
'''CREATE TABLE users (
    user_id          INTEGER PRIMARY KEY,
    email           TEXT UNIQUE
)''')
        print('Users table created success.')
        con.execute(
'''CREATE UNIQUE INDEX user_id ON users (user_id)''')

        con.execute(
'''CREATE TABLE accounts (
    account_id   INTEGER PRIMARY KEY,
    username     TEXT UNIQUE,
    email        TEXT 
)''')

        print('Accounts table created success.')
        con.execute(
'''CREATE TABLE followers (
    account_follow   INTEGER,
    account_me     INTEGER,

    FOREIGN KEY (account_follow) REFERENCES accounts (account_id),
    FOREIGN KEY (account_me) references accounts(account_id)
)''')
        print('Followers table created success.')
        con.execute(
'''
CREATE TABLE posts (
    post_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    content     TEXT NOT NULL,
    account_id  INTEGER NOT NULL,
    likes       INTEGER,

    FOREIGN KEY (account_id) references accounts(account_id)
)''')
    print('TABLE posts CREATED SUCCESSFULLY')
    con.execute(
'''
CREATE TABLE comments (
    comment_id  INTEGER PRIMARY KEY,
    content     TEXT NOT NULL,
    account_id  INTEGER NOT NULL,
    post_id     INTEGER NOT NULL,

    FOREIGN KEY (account_id) references accounts(account_id),
    FOREIGN KEY (post_id) references posts(post_id)
)''')
    print('TABLE comments CREATED SUCCESSFULLY')
    con.execute(
    '''
CREATE TABLE liked (
    liker_id    INTEGER,
    post_id    INTEGER,

    FOREIGN KEY (liker_id) references accounts(account_id),
    FOREIGN KEY (post_id) references posts(post_id)
)''')
    print('table liked created')
    print('database created')
    print()


# Adds a user with a given email, and assigns it an id.
@click.command()
@click.argument('email')
def adduser(email):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
        id = cursor.lastrowid
        print(f'Created user with email {email} inserted with id={id}')

# Adds an account to a email with a username, assigns it an id.
@click.command()
@click.argument('username')
@click.argument('email')
def addaccount(username, email):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO accounts (email, username) VALUES (?, ?)''', (email, username))
        con.commit()
        id = cursor.lastrowid
        print(f'Created account with username {username} for email {email} inserted with id={id}')

# Creates a 'follow' link from one account to another. Does not make a 2 way link,
# meaning both accounts must follow eachother before they will be linked 2 ways.
@click.command()
@click.argument('follower_id')
@click.argument('followed_id')
def follow(follower_id, followed_id):
    print(f'Account {follower_id} is now following Account {followed_id}')
    with getdb() as con:
        cursor = con.cursor()
        # Include error handling for if one or both accounts don't exits.
        cursor.execute('''SELECT 1 from accounts where account_id = ?''', (follower_id,))
        record = cursor.fetchone()
        if not record:
            print(f'Follower account {follower_id} does not exist. Exiting...')
            return
        
        cursor.execute('''SELECT 1 from accounts where account_id = ?''',(followed_id,))
        record = cursor.fetchone()
        if not record:
            print(f'Account to follow: {followed_id}, does not exist. Exiting...')
            return

        cursor.execute('''INSERT INTO followers (account_follow, account_me) VALUES (?, ?)''', (followed_id, follower_id))
        id = cursor.lastrowid

# Creates a post linked to an account. Posts will be assigned an id for lookup. Posts
# will have 'content' to fill them, and a likes field, which starts at 0.
@click.command()
@click.argument('account_id')
@click.argument('content')
def post(account_id, content):
    print(f'User {account_id} posted {content}')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO posts (account_id, content, likes) VALUES (?, ?, ?)''', (account_id, content, 0))
        id = cursor.lastrowid 
        print(f'Inserted with id={id}')

# Creates a comment on a post. Post_id must be given to create the link, and content is needed as well.
# Requires the commenters account id to be added for lookup.
@click.command()
@click.argument('post_id')
@click.argument('account_id')
@click.argument('content')
def comment(post_id, account_id, content):
    print(f'User {account_id} commented {content} on post {post_id}')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO comments (post_id, account_id, content) VALUES (?, ?, ?)''', (post_id, account_id, content))
        id = cursor.lastrowid
        print(f'Added comment with id={id}')

# 'Likes" a given post. Requires a 'liker_id' to identify who liked the post, and future implementation
# should limit each 'liker_id' to only like each post once.
@click.command()
@click.argument('post_id')
@click.argument('liker_id')
def like(post_id, liker_id):
    print(f'user {liker_id} liked the post {post_id}')
    with getdb() as con:
        cursor = con.cursor()
        
        # Check if the user has already liked the post
        cursor.execute('''SELECT * FROM liked WHERE liker_id = ? AND post_id = ?''', (liker_id, post_id))
        record = cursor.fetchone()
        
        if record:
            print("User already liked the post")
        else:
            # Increment the likes count in the posts table
            cursor.execute('''UPDATE posts SET likes = likes + 1 WHERE post_id = ?''', (post_id,))
            # Insert the like record into the liked table
            cursor.execute('''INSERT INTO liked (liker_id, post_id) VALUES (?, ?)''', (liker_id, post_id))
            print("Liked successfully")

@click.command()
@click.argument('post_id')
@click.argument('liker_id')
def unlike(post_id, liker_id):
    print(f'user {liker_id} unliked post {post_id}')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * from liked where liker_id = ? and post_id = ?''', (liker_id, post_id))

        record = cursor.fetchone()
        if record:
            cursor.execute('''UPDATE posts set likes = likes - 1 where post_id = ?''', (post_id,))
            cursor.execute('''DELETE from liked WHERE liker_id = ? AND post_id = ?''', (liker_id, post_id))
        else:
            print("\tNo like record found, exiting...")

@click.command()
@click.argument('follower_id')
@click.argument('account_id')
def unfollow(follower_id, account_id):
    print(f'account {follower_id} unfollowed account {account_id}')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT 1 from accounts where account_id = ?''', (follower_id,))
        record = cursor.fetchone()
        if not record:
            print(f'Follower account {follower_id} does not exist. Exiting...')
            return
        
        cursor.execute('''SELECT 1 from accounts where account_id = ?''',(account_id,))
        record = cursor.fetchone()
        if not record:
            print(f'Account to unfollow: {account_id}, does not exist. Exiting...')
            return
        
        cursor.execute('''SELECT * from followers where account_follow = ? and account_me = ?''', (account_id, follower_id))

        record = cursor.fetchone()
        if record:
            cursor.execute('''DELETE from followers where account_follow = ? and account_me = ?''', (account_id, follower_id))
        else:
            print(f'\taccount {follower_id} does not follow account {account_id}, aborting...')


# Below is only queries, write implementation above.
@click.command()
def users():
    print("\nUsers Registered")
    print("---------------------------------------")
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''
    SELECT * FROM users
''')
    records = cursor.fetchall()
    for row in records:
        print("User id:", row[0], "email:", row[1])
        print("---------------------------------------")
    print()

@click.command()
def accounts():
    print("\nAccounts Created")
    print("-----------------------------------------------------")
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''
    SELECT * FROM accounts
''')
    records = cursor.fetchall()
    for row in records:
        print("Account Id:", row[0], "Username:", row[1], "Email:", row[2])
        print("--------------------------------------------------------")
    print()

@click.command()
@click.argument('email')
def multi(email):
    print("\nAll accounts associated with a given email.")
    print("----------------------------------------------------")
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''
    SELECT username, email FROM accounts 
        WHERE email = ?''', (email,))
    records = cursor.fetchall()
    for row in records:
        print("Email:", row[1], "Username:", row[0])
        print("-----------------------------------------------------")
    print()

@click.command()
def follows():
    print("\nAll follow links.")
    print("--------------------")
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''
    SELECT account_follow, account_me from followers ORDER BY account_me asc
''')
    records = cursor.fetchall()
    for row in records:
        print("Account", row[1], "follows", row[0])
        print("--------------------")
    print()

@click.command()
def posts():
    print("\nAll Posts.")
    print("------------------------------------------------------------------------")
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * from posts''')
        records = cursor.fetchall()
        for row in records:
            print("post:", row[0], "says:" , row[1], "posted by account:", row[2], "with likes:", row[3])
            print("--------------------------------------------------------------------------")
        print()

@click.command()
def comments():
    print("\nAll Comments.")
    print("-------------------------------------------------------------------------")
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * from comments''')
        records = cursor.fetchall()
        for row in records:
            print("Comment:", row[0], "says: '", row[1], "' posted by account:", row[2], "on post:", row[3])
            print("--------------------------------------------------------------------------")
        print()

@click.command()
def gossip():
    print("\nReturn popular posts, ranked by #likes")
    print("-----------------------------------------------------")
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''
SELECT p.post_id, p.account_id, p.content, p.likes 
    FROM posts p
    ORDER BY p.likes desc
''')
        records = cursor.fetchall()
        for row in records:
            print("post:",row[0], "by account:",row[1], "content:",row[2], "popularity:",row[3])

@click.command()
@click.argument('account_id')
def stalker(account_id):
    print(f"Finding who has the most interest in account {account_id}")
    print('--------------------------------------------')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''
SELECT me.account_id, s.account_id, count(1) as interest
    FROM accounts me 
    JOIN posts p on me.account_id = p.account_id
    JOIN liked l on p.post_id = l.post_id
    JOIN accounts s on s.account_id = l.liker_id
    where me.account_id = ?
    GROUP BY s.account_id
    ORDER BY interest desc
''', (account_id,))
        records = cursor.fetchall()
        for row in records:
            print("account:",row[1], "interest:", row[2], "on account:", row[0])

@click.command()
def delete():
    print("Deleting the universe")
    os.remove("network.db")
    print("Universe deleted")

# add commands
cli.add_command(create)
cli.add_command(adduser)
cli.add_command(addaccount)
cli.add_command(follow)
cli.add_command(post)
cli.add_command(comment)
cli.add_command(like)
cli.add_command(unlike)
cli.add_command(unfollow)
cli.add_command(delete)

# add queries
cli.add_command(users)
cli.add_command(accounts)
cli.add_command(multi)
cli.add_command(follows)
cli.add_command(posts)
cli.add_command(comments)
cli.add_command(gossip)
cli.add_command(stalker)

cli()
