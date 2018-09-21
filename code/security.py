from user import User
# users = [
#     User(1, 'bob', 'asdf')
# ]
#
# username_mapping = { u.username: u for u in users}
# # username_mapping {'bob': {
# #         'id': 1,
# #         'username': 'bob',
# #         'password': 'asdf'
# #     }
# # }
# userid_mapping = { u.id: u for u in users }
# # userid_mapping = { 1: {
# #         'id': 1,
# #         'username': 'bob',
# #         'password': 'asdf'
# #     }
# # }


def authenticate(username, password):
    # .get is another way of accessing a dictionary
    # similar to
    # username_mapping['username']
    user = User.find_by_username(username)
    if user and user.password == password:
        return user

# unique to flask jwt
# takes a payload, which is the contents of the jwt token
# identity is called when we pass the token generated from /auth to whatever
# requires the id

def identity(payload):
    print("ive been called")
    print(payload)
    user_id = payload['identity']
    print(user_id)
    # extract used_id from payload
    # return userid_mapping.get(user_id, None)
    return User.find_by_id(user_id)
