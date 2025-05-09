#!/usr/bin

# Create the database
rm -f network.db
sqlite3 network.db<schema.sql

# create users
python3 social.py adduser example1@email.com
python3 social.py adduser john.doe@email.com
python3 social.py adduser jane.smith@email.com
python3 social.py adduser example2@email.com
python3 social.py adduser alexander@email.com
python3 social.py adduser sarahmiller@email.com
python3 social.py adduser example3@email.com
python3 social.py adduser maxwell@email.com
python3 social.py adduser emily.wong@email.com
python3 social.py adduser example4@email.com
python3 social.py adduser chris@email.com
python3 social.py adduser lisa.smiles@email.com
python3 social.py adduser example5@email.com
python3 social.py adduser samantha@email.com
python3 social.py adduser tom.jones@email.com
# Retrieve all accounts
python3 social.py users

# create accounts

python3 social.py addaccount user123 example1@email.com
python3 social.py addaccount user321 example1@email.com

python3 social.py addaccount john_doe john.doe@email.com

python3 social.py addaccount jane_smith jane.smith@email.com
python3 social.py addaccount jannett_smithington jane.smith@email.com

python3 social.py addaccount user456 example2@email.com
python3 social.py addaccount alex_89 alexander@email.com
python3 social.py addaccount sarah_miller sarahmiller@email.com
python3 social.py addaccount user789 example3@email.com

python3 social.py addaccount maxwell_22 maxwell@email.com
python3 social.py addaccount beef_maxwellington maxwell@email.com

python3 social.py addaccount emily_wong emily.wong@email.com
python3 social.py addaccount user101 example4@email.com
python3 social.py addaccount chris_007 chris@email.com
python3 social.py addaccount lisa_smiles lisa.smiles@email.com
python3 social.py addaccount user202 example5@email.com
python3 social.py addaccount samantha23 samantha@email.com
python3 social.py addaccount tom_jones tom.jones@email.com
# Retrieve all created accounts
python3 social.py accounts
# Retrieve all accounts associated with a given user.
python3 social.py multi example1@email.com
python3 social.py multi jane.smith@email.com
python3 social.py multi maxwell@email.com




# Create follow links between accounts using the 'follow' command.
python3 social.py follow 1 2
python3 social.py follow 2 3
python3 social.py follow 2 1
python3 social.py follow 10 9
python3 social.py follow 8 4
python3 social.py follow 7 2
python3 social.py follow 6 1
python3 social.py follow 12 4
python3 social.py follow 4 12
python3 social.py follow 4 2

python3 social.py follow 14 11

python3 social.py follow 100 1
python3 social.py follow 1 100

python3 social.py follows
python3 social.py unfollow 1 2
python3 social.py unfollow 14 11
python3 social.py unfollow 10 9
python3 social.py unfollow 2 1
python3 social.py unfollow 6 1
python3 social.py unfollow 6 10
python3 social.py follows

# Create posts from different accounts
python3 social.py post 12 "I'm excited for my birthday."
python3 social.py post 2 "I don't want to go to school."
python3 social.py post 9 "I fought a hippo."
python3 social.py post 3 "No one told me there wasn't school today."
python3 social.py post 7 "Live. Die. Repeat."
python3 social.py post 12 "3 days until my bday"
python3 social.py post 12 "D"
python3 social.py post 12 "C"
python3 social.py post 12 "B"
python3 social.py post 12 "A"
python3 social.py post 2 "I skipped school."
python3 social.py posts

# Comment on different posts from a commenter
python3 social.py comment 1 7 "Happy Birthday!"
python3 social.py comment 4 11 "There isn't school today. you're welcome"
python3 social.py comment 7 6  "Congrats"
python3 social.py comment 1 3 ":)"
python3 social.py comments

# Add likes on comments.
python3 social.py like 1 11
python3 social.py like 2 11
python3 social.py like 2 9
python3 social.py like 3 12
python3 social.py like 1 4
python3 social.py like 6 7
python3 social.py like 6 9
python3 social.py like 5 11
python3 social.py like 1 11
python3 social.py like 1 2
python3 social.py like 1 3
python3 social.py like 7 5
python3 social.py like 8 5
python3 social.py like 9 5
python3 social.py like 10 5

python3 social.py gossip

python3 social.py posts

python3 social.py unlike 1 11
python3 social.py unlike 2 11
python3 social.py unlike 6 7
python3 social.py unlike 6 9
python3 social.py unlike 6 10
python3 social.py unlike 3 8
python3 social.py unlike 1 2

python3 social.py posts

python3 social.py stalker 12



