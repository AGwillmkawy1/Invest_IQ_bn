"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.
"""
# in production api we use database or reddis
BLOCKLIST = set()
all_login_users = {}