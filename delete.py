import os
import json

string_dict = os.getenv("DATABASE")
convertedDict = json.loads(string_dict)


print(type(convertedDict))
print(convertedDict['host'])
