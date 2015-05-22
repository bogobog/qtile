
import math

from libqtile.widget import GroupBox
from .drop_down_box import DropDownBoxChild

__all__ = [ 'DropDownGroupBox', ]

class DropDownGroupBoxChild( DropDownBoxChild ):

    def _configure( self, qtile, screen ):
        DropDownBoxChild._configure( self, qtile, screen )

        self.window.handle_ButtonRelease = self.handle_ButtonRelease

    def getWindowItem( self, x, y ):
        per_item_size = self.height / len( self.parent.active_group_windows )
        item_index = int( math.floor( float( y ) / per_item_size ) )

        return self.parent.active_group_windows[ item_index ]

    def handle_ButtonRelease( self, e ):

        if e.detail == 1:
            self.parent.bar.screen.setGroup( self.parent.active_group )
            window = self.getWindowItem( e.event_x, e.event_y )

            if window.minimized:
                window.disablefloating()

            window.group.focus( window, False )

            if window.floating:
                window.cmd_bring_to_front()

            self.parent.active_group_windows = []
            self.parent.active_group = None

        DropDownBoxChild.handle_ButtonRelease( self, e )

class DropDownGroupBox( GroupBox ):

    def __init__( self, *args, **kwargs ):
        GroupBox.__init__( self, *args, **kwargs )

        self.active_group_windows = []
        self.active_group = None

    def button_press( self, x, y, button ):
        if not button == 3:
            GroupBox.button_press( self, x, y, button )

    def button_release( self, x, y, button ):
        if button == 3:
            clicked_group = self.get_clicked_group( x, y )

            if not len( clicked_group.windows ) or clicked_group == self.active_group:
                self.active_group_windows = []
                self.active_group = None
                self.child.window.hide()
                return

            self.active_group_windows = list( clicked_group.windows )

            processed_child_text = []
            for win in self.active_group_windows:
               if win.minimized:
                  processed_child_text.append( '<span fgcolor="darkgray">%s</span>' % win.name.encode( 'ascii', 'ignore' ) )
               else:
                  processed_child_text.append( win.name.encode( 'ascii', 'ignore' ) )

            self.child.text = '\n'.join( processed_child_text )

            self.child.window.unhide()

            self.active_group = clicked_group
        else:
            self.active_group_windows = []
            self.active_group = None
            self.child.window.hide()
            GroupBox.button_release( self, x, y, button )

    def _configure( self, qtile, screen ):
        GroupBox._configure( self, qtile, screen )    
    
        self.borderwidth = 0
        self.padding_y = 0
        self.margin_y = -2

        self.child = DropDownGroupBoxChild( self )
        self.child._configure( qtile, screen )
        self.child.text = ''


# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
