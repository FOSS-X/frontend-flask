# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
 
import hashlib, binascii, os
from functools import wraps
from flask import redirect, url_for, session
import requests
# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

UDAPI_URL = "http://localhost:2020"


# def hash_pass( password ):
#     """Hash a password for storing."""
#     salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
#     pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
#                                 salt, 100000)
#     pwdhash = binascii.hexlify(pwdhash)
#     return (salt + pwdhash) # return bytes

# def verify_pass(provided_password, stored_password):
#     """Verify a stored password against one provided by user"""
#     stored_password = stored_password.decode('ascii')
#     salt = stored_password[:64]
#     stored_password = stored_password[64:]
#     pwdhash = hashlib.pbkdf2_hmac('sha512', 
#                                   provided_password.encode('utf-8'), 
#                                   salt.encode('ascii'), 
#                                   100000)
#     pwdhash = binascii.hexlify(pwdhash).decode('ascii')
#     return pwdhash == stored_password

def verify_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        url = UDAPI_URL + "/verifyuser"
        headers = {'jwtToken': session['jwtToken']}
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            if data['verified']:
                pass
        except:
            return redirect(url_for('base_blueprint.logout'))
        return f(*args, **kwargs)
    return decorated