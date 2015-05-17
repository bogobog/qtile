#!/bin/sh

. /home/judar/bin/qtile/volume_common

amixer -q sset Master toggle
update_volume
