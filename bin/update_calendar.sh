#!/bin/sh

cal --color=always | sed -e 's:\x1B\[7m:<span bgcolor="blue">:g' -e 's:\x1B\[27m:</span>:g' > /dev/shm/qtile_timedropdownbox_child
