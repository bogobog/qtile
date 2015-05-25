
import time
import dbus

from .markup_threaded_poll_text import MarkupThreadedPollText

GLOBAL_STATE_COLORS = [ '#737373', 'red', '#b2b200', '#ff9900', 'green' ]
GLOBAL_STATE_ICON = [ '?', 'v', 'v', '*', '^' ]
CONNECTION_STATE_COLORS = [ '#737373', '#b2b200', 'green', '#ff9900', '#737373' ]
BUS_NAME = 'org.freedesktop.NetworkManager'

class NetworkStatusBox( MarkupThreadedPollText ):

    defaults = [
        ("update_interval", 5, "Update interval in seconds, if none, the "
            "widget updates whenever the event loop is idle."),
    ]

    def __init__( self, *args, **kwargs ):
        MarkupThreadedPollText.__init__( self, *args, **kwargs )
        self.add_defaults( NetworkStatusBox.defaults )

    def poll( self ):
        output = []

        bus = dbus.SystemBus()

        nm = bus.get_object( BUS_NAME, '/org/freedesktop/NetworkManager' )

        device_list = nm.Get( BUS_NAME, 'Devices' )
        global_state = nm.Get( BUS_NAME, 'Connectivity' )

        output.append( '<span bgcolor="%s">%s</span>' % ( GLOBAL_STATE_COLORS[ int( global_state ) ], GLOBAL_STATE_ICON[ int( global_state ) ] ) )

        for dev in device_list:
            device = bus.get_object( BUS_NAME, dev )
            name = device.Get( 'org.freedesktop.NetworkManager.Device', 'Interface' )
    
            if name == 'lo':
                continue

            ac_path = device.Get( 'org.freedesktop.NetworkManager.Device', 'ActiveConnection' )
            if ac_path == '/':
                state_color = CONNECTION_STATE_COLORS[ 4 ] 
            else:
                ac = bus.get_object( BUS_NAME, str( ac_path ) )
                ac_state = ac.Get( 'org.freedesktop.NetworkManager.Connection.Active', 'State' )
                state_color = CONNECTION_STATE_COLORS[ int( ac_state ) ]

            output.append( '<span bgcolor="%s">%s</span>' % ( state_color, name ) )

        return ' '.join( output ).encode( 'ascii', 'ignore' )

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
