#!/bin/sh

hostname=$( hostname -s )

. ${HOME}/.config/qtile/custom/configs/startup.${hostname}

startup
