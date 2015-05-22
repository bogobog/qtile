#!/bin/sh

global_status=$( nm-tool | grep '^State' | awk '{ print $2 }' )

if [ "${global_status}" = 'connected' ]; then
    current_devices=$( nm-tool | grep -E ' (Device|State)' | grep -B1 connected | grep Device | awk '{ print $3 }' | xargs )
    output="<span bgcolor=\"darkgreen\">${current_devices}</span>"
else
    output="<span bgcolor=\"red\">Down</span>"
fi

echo $output > /dev/shm/qtile_networkstatusbox