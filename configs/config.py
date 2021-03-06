
import os
import subprocess
import imp
import socket
import re

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

import custom

mod = "mod4"
home = os.path.expanduser('~')

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

    # Swap panes of split stack
    Key(
        [mod, "shift"], "Down",
        lazy.window.enable_minimize()
    ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawn("dmenu_run -i -fn '-*-droid sans-medium-*-*-*-13-*-*-*-*-*-*-*' -nb '#737373' -nf '#000000'")),

    # lock screen
    Key([mod], "l", lazy.spawn( home + "/bin/qtile/lock.sh" ) ),

]

groups = [ Group(i) for i in "kwdmc" ]

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
    custom.SmallerMonadTall(ratio=0.15)
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
    "vpnui",
  ) ]
)

widget_defaults = dict(
    font='Droid Sans Mono',
    fontsize=15,
    padding=3,
)

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
def autostart_once():
    subprocess.call([home + '/.config/qtile/startup_once.sh'])

@hook.subscribe.startup
def autostart():
    subprocess.call([home + '/.config/qtile/startup.sh'])

@hook.subscribe.client_new
def client_new( c ):
    if c.window.get_wm_class():
        if 'Pidgin' in c.window.get_wm_class():
            c.togroup( 'c' )
        elif 'konsole' in c.window.get_wm_class():
            c.togroup( 'k' )
        elif 'Firefox' in c.window.get_wm_class():
            if re.search( 'Outlook Web App', c.window.get_name() ):
                c.togroup( 'm' )
            else:
                c.togroup( 'w' )

local_config = imp.load_source( 'local_config', '%s/.config/qtile/custom/configs/config.%s.py' % ( home, socket.gethostname().split('.')[0] ) )

if hasattr( local_config, 'keys' ):
    keys.extend( local_config.keys )

screens = local_config.screens

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
