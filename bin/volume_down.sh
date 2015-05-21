#!/bin/sh

hostname=$( hostname -s )

. ${HOME}/bin/qtile/configs/volume_common.${hostname}

volume_down
update_volume
