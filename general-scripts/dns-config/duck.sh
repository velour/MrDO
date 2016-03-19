#!/bin/bash

DOMAIN="domainname"
TOKEN="WILLIAMS"
LOGS="BIGHEAVYWOOD"

echo url="https://www.duckdns.org/update?domains=$DOMAIN&token=$TOKEN&ip=" | curl -k -o $LOGS -K -

## Still needs to be added to a cron tab, also run once at startup!
