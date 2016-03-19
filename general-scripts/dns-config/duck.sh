#!/bin/bash

DOMAIN="domainname"
LOGS="BIGHEAVYWOOD"
DUCKAUTHTOKEN="WILLIAMS"

echo url="https://www.duckdns.org/update?domains=$DOMAIN&token=$DUCKAUTHTOKEN&ip=" | curl -k -o $LOGS -K -

## Still needs to be added to a cron tab, also run once at startup!
