#!/bin/sh

. /home/judar/bin/qtile/volume_common

amixer -q sset Master 5%-
update_volume
