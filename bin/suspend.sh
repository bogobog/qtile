#!/bin/sh

hostname=$( hostname -s )

. ${HOME}/bin/qtile/configs/suspend.${hostname}

suspend_system
