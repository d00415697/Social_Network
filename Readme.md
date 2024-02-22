Project Social Networks
Partners: De'ray Lowe & Luke Geyer

######################################################################################################################################################################

Tables:
- Users
- Accounts
- Followers
- Posts

Features:
- Likes
- Comments

What we did:
    - We created a like feature that uses a count method. Everytime a user "likes" the accounts post it adds plus one. we added a little extra to make sure the user couldn't repetitivly like the post more then once, but they could remove the like as well if they wished to.
    
    - We created a comment feature that allows for text commentary. The comments are linked to the post for others to view.  

Queries:

1. Gossip:
   - Write a query that shows the most interesting topics on the feed based on number of likes. 
2. Stalker
    - Write a query that shows that shows compatibility rate from users who likes your post frequently.

Functions:
    -Adduser(email)
        Descrip: Adds the user's information.
    
    -Addaccount(username, email)
        Descrip: Creates a new account for the user using the username and email.
    
    -Follow(follower_id, followed_id)
        Descrip: Creates a memory bank of people that follow the user.
    
    -Post(account_id, content)
        Descrip: Makes a post on the feed with content included from the user. 
    
    -Comment(post_id, account_id, content)
        Descrip: Create and post a coment in the feed from the user using the user's post/account id and content.
    
    -Like(post_id, liker_id)
        Descrip: Adds 1 "Like" to the user's post one time from each follower
    
    -Unlike(post_id, liker_id)
        Descrip: Delete the like from the user's account 
    
    -Delete()
        Descrip: Wipes the network.db 
    
    -Unfollow(follower_id, account_id)
        Descrip:  Unfollow the current user