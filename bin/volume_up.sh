#!/bin/sh

hostname=$( hostname -s )

. ${HOME}/bin/qtile/configs/volume_common.${hostname}

volume_up
update_volume
