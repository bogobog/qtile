#!/bin/sh

hostname=$( hostname -s )

. ${HOME}/.config/qtile/custom/configs/startup_once.${hostname}

startup_once
