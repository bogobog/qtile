#!/bin/sh

export TERM=xterm-256color

script -q /dev/null -c cal | sed -e 's:\x1B\[7m:<span bgcolor="blue">:g' -e 's:\x1B\[27m:</span>:g' > /dev/shm/qtile_timedropdownbox_child
