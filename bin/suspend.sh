#!/bin/sh

# before
xscreensaver-command -lock
pkill -f keepass

sleep 2
sudo systemctl suspend

# after
/home/judar/bin/qtile/update_calendar.sh
/home/judar/bin/qtile/update_time.sh
/home/judar/bin/qtile/update_volume.sh
