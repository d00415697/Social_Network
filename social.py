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
    print('database created')

# Adds a user with a given email, and assigns it an id.
@click.command()
@click.argument('email')
def adduser(email):
    print('created user with email', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
        id = cursor.lastrowid
        print(f'inserted with id={id}')

# Adds an account to a email with a username, assigns it an id.
@click.command()
@click.argument('username')
@click.argument('email')
def addaccount(username, email):
    print('creating account with username', username, 'for email', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO accounts (email, username) VALUES (?, ?)''', (email, username))
        con.commit()
        id = cursor.lastrowid
        print(f'inserted with id={id}')

# Creates a 'follow' link from one account to another. Does not make a 2 way link,
# meaning both accounts must follow eachother before they will be linked 2 ways.
@click.command()
@click.argument('follower_id')
@click.argument('followed_id')
def follow(follower_id, followed_id):
    print(f'Account {follower_id} is now following Account {followed_id}')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO followers (account_follow, account_me) VALUES (?, ?)''', (followed_id, follower_id))
        id = cursor.lastrowid
        print(f'Follow successful with id={id}')

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
        cursor.execute('''Update posts set likes = likes + 1 where post_id = ?  ''', (post_id))
        print('liked successfully')


# Below is only queries, write implementation above.
@click.command()
def query0():
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
def query1():
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
def query2(email):
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
def query3():
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


cli.add_command(create)
cli.add_command(adduser)
cli.add_command(addaccount)
cli.add_command(follow)
cli.add_command(post)
cli.add_command(comment)
cli.add_command(like)

cli.add_command(query0)
cli.add_command(query1)
cli.add_command(query2)
cli.add_command(query3)

cli()
