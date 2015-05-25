
import os

from libqtile.config import Screen, Key
from libqtile.command import lazy
from libqtile import bar, widget

import custom

mod = "mod4"
home = os.path.expanduser('~')

keys = [
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn( home + "/bin/qtile/volume_up.sh" )
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn( home + "/bin/qtile/volume_down.sh" )
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn( home + "/bin/qtile/volume_toggle.sh" )
    ),
    Key(
        [mod, 'control', 'shift'], "F4",
        lazy.spawn( home + "/bin/qtile/suspend.sh" )
    ),
]

menu_one_menu_items = [
    { 'name': 'Apelint',
      'command': 'apelint_wireless.sh',
    },
]

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.Systray(),
                custom.BlackSep(),
                widget.Battery(),
                custom.BlackSep(),
                custom.CommandTextBox( name = 'VolumeTextBox', command = home + '/bin/qtile/volume_toggle.sh' ),
                custom.BlackSep(),
                custom.DropDownBox( name = 'TimeDropDownBox' ),
                custom.BlackSep(),
                custom.DropDownGroupBox( highlight_method = 'block', rounded = False, disable_drag = True, ),
                custom.BlackSep(),
                widget.Spacer( width = bar.STRETCH ),
                custom.BlackSep(),
                custom.NetworkStatusBox(),
            ],
            20,
            background = '#737373',
        ),
    ),
]

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
