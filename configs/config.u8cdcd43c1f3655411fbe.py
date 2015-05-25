
import os

from libqtile.config import Screen
from libqtile import bar, widget

import custom

home = os.path.expanduser('~')

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.Systray(),
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
