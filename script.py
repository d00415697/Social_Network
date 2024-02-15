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
    username     TEXT NOT NULL,
    email           TEXT NOT NULL
)''')
        print('Users table created success.')
        con.execute(
'''CREATE UNIQUE INDEX user_id ON users (user_id)''')

        con.execute(
'''CREATE TABLE accounts (
    account_id   INTEGER PRIMARY KEY,
    user_id      INTEGER NOT NULL,
    username     TEXT NOT NULL,
    email        TEXT NOT NULL,

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
    post_id     INTEGER PRIMARY KEY,
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
@click.argument('username')
def adduser(username):
    print('creating user with name ', username)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO users (username) VALUES (?)''', (username,))
        id = cursor.lastrowid
        print(f'inserted with id={id}')

@click.command()
@click.argument('email')
@click.argument('username')
def addaccount(username, email):
    print('creating account with username', username, 'for email', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO accounts (user_id, username)
VALUES ((SELECT user_id FROM users WHERE email = ?), ?)''', (email, username))
        id = cursor.lastrowid
        print(f'inserted with id={id}')

cli.add_command(create)
cli.add_command(adduser)
cli.add_command(addaccount)
cli()
