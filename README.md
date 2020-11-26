# broadlink-ac-rest-service

# Info
Web-service that allows to control Vortex smart ac units via REST.

**WARNING: This is just a prototype project not a final product!**<br>
Even if the API's work, 
I din't spend any time to handle all the possible inputs & exceptions.   
Consider-it the minimum effort to make things work. 

# Compatibility
 - Vortex VORTEX VAI-A1217FJW
 
The library that was modified from, supported also these devices (so it's a high chance for them to work):
 - Dunham bush
 - Rcool Solo
 - Akai 9000BTU
 - Rinnai
 - Kenwood
 - Tornado X (2019 and up)
 - AUX ASW-H09A4/DE-R1DI (Broadlink module)
 - Ballu BSUI/IN-12HN8 

In general, it should support the smart AC units that have the AcFreedom app. 

If you have tested this on other devices, please let me know, to update this readme.

# Configuration
Modify the config.yml according to your specs.

# Pre-requirements
```
pip install pyyaml
pip install PyCrypto
```

# Configuration
Copy the config_sample.yaml to config.yaml & change the variables. 

# Running the service
```
python3 server.py
```

# APIs

| VERB | ROUTE | DESCRIPTION | Bearer token auth | x-device-mac header | command-param body json | 
| ---- | ----- | ----------- | ----------------- | ------------------- | ---- |
| GET | / | Welcome page | No | No | None | 
| GET | /ac/discover | Discover the devices connected to the same network | Yes | No | None |
| GET | /ac/list | List the devices that were loaded from the config | Yes | No | None |
| GET | /ac/status | Get the status of one AC unit | Yes | Yes | None
| POST | /ac/command | Send a command-param set to one ac unit | Yes | Yes | Yes

# Commands & Parameters examples 
```
{"command":"power","param":"on"}
{"command":"power","param":"off"}
{"command":"temperature","param":"20"}
{"command":"mode","param":"cooling"}
{"command":"mode","param":"dry"}
{"command":"mode","param":"heating"}
{"command":"mode","param":"auto"}
{"command":"mode","param":"fan"}
```

# Example 
```
curl --location --request POST 'http://localhost:9000/ac/command' \
--header 'Authorization: Bearer REPLACE_ME' \
--header 'x-device-mac: 34:EA:AA:AA:AA:AA' \
--header 'Content-Type: application/json' \
--data-raw '{"command":"mode","param":"cooling"}'
```

# Tags: 
IOT, SmartHome

# Credits
ac_db.py is a modified version from: https://github.com/liaan/broadlink_ac_mqtt
