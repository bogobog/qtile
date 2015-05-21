#!/bin/sh

global_status=$( nm-tool | grep '^State' | awk '{ print $2 }' )

if [ "${global_status}" = 'connected' ]; then
    current_device=$( nm-tool | grep 'Device' | awk '{ print $3 }' )
    output="<span bgcolor=\"darkgreen\">${current_device}</span>"
else
    output="<span bgcolor=\"red\">Down</span>"
fi

echo $output > /dev/shm/qtile_networkstatusbox
