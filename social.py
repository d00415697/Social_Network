'''#!/usr/bin/env python3'''

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
    email           TEXT NOT NULL
)''')
        print('Users table created success.')
        con.execute(
'''CREATE UNIQUE INDEX user_id ON users (user_id)''')

        con.execute(
'''CREATE TABLE accounts (
    account_id   INTEGER PRIMARY KEY,
    user_id      INTEGER,
    username     TEXT,
    email        TEXT,

    FOREIGN KEY (user_id) references users(user_id)
)''')

        print('Accounts table created success.')
        con.execute(
'''CREATE TABLE followers (
    account_follow   INTEGER PRIMARY KEY,
    account_me     INTEGER NOT NULL,

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

@click.command()
@click.argument('email')
def adduser(email):
    print('created user with email', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
        id = cursor.lastrowid
        print(f'inserted with id={id}')

@click.command()
@click.argument('email')
@click.argument('username')
def addaccount(username, email):
    print('creating account with username', username, 'for email', email)
    with getdb() as con:
        cursor = con.cursor()
        id = cursor.lastrowid
        cursor.execute('''INSERT INTO accounts (email, account_id, username)
VALUES ((SELECT user_id FROM users WHERE email = ?), ?)''', (email,id, username))
        print(f'inserted with id={id}')

@click.command()
@click.argument('follower_id')
@click.argument('followed_id')
def follow(follower_id, followed_id):
    print(f'User {follower_id} is now following User {followed_id}')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO followers (account_follow, account_me) VALUES (?, ?)''', (followed_id, follower_id))
        id = cursor.lastrowid
        print(f'Follow successful with id={id}')

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

@click.command()
@click.argument('post_id')
@click.argument('liker_id')
def like(post_id, liker_id):
    print(f'user {liker_id} liked the post {post_id}')
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''Update posts set likes = likes + 1 where post_id = ?  ''', (post_id))
        print('liked successfully')

@click.command()
def query1():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''
    SELECT * FROM accounts
''')
    records = cursor.fetchall()
    for row in records:
        print("Account Id: ", row[0], "User Id: ", row[1], "Username: ", row[2], "Email: ", row[3])


cli.add_command(create)
cli.add_command(adduser)
cli.add_command(addaccount)
cli.add_command(follow)
cli.add_command(post)
cli.add_command(comment)
cli.add_command(like)
cli.add_command(query1)
cli()
