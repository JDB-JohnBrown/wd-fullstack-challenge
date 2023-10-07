# services\jsonClassEncoder.py
# Directly borrowed from https://medium.com/@andrelbaldo/register-login-and-logout-boilerplate-written-in-vue-js-and-python-as-api-5ce57e33774b
# No changes neccessary
# Author : Andre Baldo (http://github.com/andrebaldo/)
# A default encoder, it will read the class properties and retur it as a dictionary, 
# so the json serializer can convert it
from json import JSONEncoder
class JsonClassEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__  