
import dbus

from .markup_threaded_poll_text import MarkupThreadedPollText

class NetworkStatusBox( MarkupThreadedPollText ):

    GLOBAL_STATE_COLORS = [ '#737373', 'red', 'red', 'red', '#b2b200', '#ff9900', '#ff9900', 'darkgreen' ]
    GLOBAL_STATE_ICON = [ '?', 'v', 'v', 'v', '*', '^', '^', '^' ]
    CONNECTION_STATE_COLORS = [ '#737373', '#b2b200', 'darkgreen', '#ff9900', '#737373' ]
    BUS_NAME = 'org.freedesktop.NetworkManager'
    CLICK_COMMAND = '/bin/kde-nm-connection-editor'

    defaults = [
        ("update_interval", 5, "Update interval in seconds, if none, the "
            "widget updates whenever the event loop is idle."),
    ]

    def __init__( self, *args, **kwargs ):
        MarkupThreadedPollText.__init__( self, *args, **kwargs )
        self.add_defaults( NetworkStatusBox.defaults )
        self.bus = dbus.SystemBus()

    def button_release( self, x, y, button ):
        self.qtile.cmd_spawn( self.CLICK_COMMAND )

    def poll( self ):
        output = []

        nm = self.bus.get_object( self.BUS_NAME, '/org/freedesktop/NetworkManager' )

        device_list = nm.GetDevices()

        global_state = nm.state()
        global_state = ( global_state > 0 and global_state / 10 ) or global_state

        output.append( '<span bgcolor="%s">%s</span>' % ( self.GLOBAL_STATE_COLORS[ int( global_state ) ], self.GLOBAL_STATE_ICON[ int( global_state ) ] ) )

        for dev in device_list:
            device = self.bus.get_object( self.BUS_NAME, dev )
            name = device.Get( 'org.freedesktop.NetworkManager.Device', 'Interface' )
    
            if name == 'lo':
                continue

            ac_path = device.Get( 'org.freedesktop.NetworkManager.Device', 'ActiveConnection' )
            if ac_path == '/':
                state_color = self.CONNECTION_STATE_COLORS[ 4 ] 
            else:
                ac = self.bus.get_object( self.BUS_NAME, str( ac_path ) )
                ac_state = ac.Get( 'org.freedesktop.NetworkManager.Connection.Active', 'State' )
                state_color = self.CONNECTION_STATE_COLORS[ int( ac_state ) ]

            output.append( '<span bgcolor="%s">%s</span>' % ( state_color, name ) )

        return ' '.join( output ).encode( 'ascii', 'ignore' )

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
