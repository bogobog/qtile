
import os, subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

import custom

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "Down",
        lazy.layout.down()
    ),
    Key(
        [mod], "Up",
        lazy.layout.up()
    ),

    Key(
        [mod], "Left",
        lazy.layout.previous()
    ),

    Key(
        [mod], "Right",
        lazy.layout.next()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "Down",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "Up",
        lazy.layout.shuffle_up()
    ),
    Key(
        [mod, "control"], "Left",
        lazy.layout.client_to_next()
    ),
    Key(
        [mod, "control"], "Right",
        lazy.layout.client_to_previous()
    ),
    Key(
        [mod, "mod1"], "Up",
        lazy.layout.grow()
    ),
    Key(
        [mod, "mod1"], "Down",
        lazy.layout.shrink()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),

    Key([mod], "c", lazy.spawn("kcalc")),
    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "i", lazy.spawn("kwrite")),
    Key([mod], "k", lazy.spawn("konsole")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawn("dmenu_run -i -fn '-*-fixed-*-*-*-*-18-*-*-*-*-*-*-*' -nb '#737373' -nf '#000000'")),

    # volume
    Key( [], "XF86AudioRaiseVolume", lazy.spawn("/home/judar/bin/qtile/volume_up.sh") ),
    Key( [], "XF86AudioLowerVolume", lazy.spawn("/home/judar/bin/qtile/volume_down.sh") ),
    Key( [], "XF86AudioMute", lazy.spawn("/home/judar/bin/qtile/volume_toggle.sh") ),

    # lock screen
    Key([mod], "l", lazy.spawn("/home/judar/bin/qtile/lock.sh")),

    # suspend
    Key([mod, "control", "shift"], "F4", lazy.spawn("/home/judar/bin/qtile/suspend.sh")),
    
]

groups = [Group(i) for i in "12345"]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    custom.SmallerMonadTall()
]

floating_layout = layout.floating.Floating( float_rules = [ 
  { 'wmclass': x } for x in (
    'Download',
    'dropbox',
    'file_progress',
    "notification",
    "toolbar",
    "splash",
    "dialog",
    "keepass2",
    "kcalc",
  ) ]
)

widget_defaults = dict(
    font='Droid Sans Mono',
    fontsize=15,
    padding=3,
)

menu_one_menu_items = [
    { 'name': 'Apelint',
      'command': 'apelint_wireless.sh',
    },
    { 'name': 'Keepass',
      'command': 'keepass',
    }
]

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.Systray(),
                custom.BlackSep(),
                widget.Battery(),
                custom.BlackSep(),
                custom.CommandTextBox( name = 'VolumeTextBox', command = '/home/judar/bin/qtile/volume_toggle.sh' ),
                custom.BlackSep(),
                custom.DropDownBox( name = 'TimeDropDownBox' ),
                custom.BlackSep(),
                custom.DropDownGroupBox( highlight_method = 'block', rounded = False, disable_drag = True, ),
                custom.BlackSep(),
                widget.Spacer( width = bar.STRETCH ),
                custom.BlackSep(),
                custom.NotificationBox( name = 'NotificationBox' ),
                custom.BlackSep(),
                custom.MenuBox( name = 'MenuOneMenuBox', title = 'M1', menu_items = menu_one_menu_items ),
            ],
            20,
            background = '#737373',
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/startup_once.sh'])

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/startup.sh'])

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
