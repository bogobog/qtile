#!/bin/sh

hostname=$( hostname -s )

. ${HOME}/bin/qtile/configs/update_network_status.${hostname}

update_network_status
