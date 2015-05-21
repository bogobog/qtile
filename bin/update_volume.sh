#!/bin/sh

hostname=$( hostname -s )

. ${HOME}/bin/qtile/configs/volume_common.${hostname}

update_volume
