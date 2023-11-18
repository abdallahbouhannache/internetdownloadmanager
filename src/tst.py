import bson
import random

a=random.randint(13, 559)

json_data = {
    "winrar.exe": { "last_byte": 562, "running": True,"Time_Left":15241,"Downloaded":253612,"Speed":14525,"Url":"urlbackend.com","Size":652384 },
    "winrar-x64-623.exe": { "last_byte": 482, "running": False,"Time_Left":1241,"Downloaded":100000,"Speed":145,"Url":"urlbackend.com","Size":2202384 },
}

print(json_data)

# Convert JSON to BSON
bson_data = bson.dumps(json_data)

# Save BSON data to a file
with open('./server/download_state.bson', 'wb') as file:
    file.write(bson_data)

