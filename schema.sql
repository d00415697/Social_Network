CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY,
    email       TEXT UNIQUE
);

CREATE UNIQUE INDEX user_id ON users (user_id);

CREATE TABLE accounts (
    account_id  INTEGER PRIMARY KEY,
    username    TEXT UNIQUE,
    email       TEXT
);

CREATE TABLE followers (
    account_follow      INTEGER,
    account_me          INTEGER,

    FOREIGN KEY (account_follow) REFERENCES accounts(account_id),
    FOREIGN KEY (account_me) REFERENCES accounts (account_id)
);

CREATE TABLE posts (
    post_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    content     TEXT NOT NULL,
    account_id  INTEGER NOT NULL,
    likes       INTEGER,

    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE comments (
    comment_id  INTEGER PRIMARY KEY,
    content     TEXT NOT NULL,
    account_id  INTEGER NOT NULL,
    post_id     INTEGER NOT NULL,

    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE liked (
    liker_id     INTEGER,
    post_id      INTEGER,

    FOREIGN KEY (liker_id) REFERENCES accounts (account_id),
    FOREIGN KEY (post_id) REFERENCES posts (post_id)
);
