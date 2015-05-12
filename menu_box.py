
import math, subprocess

from .drop_down_box import DropDownBox, DropDownBoxChild

__all__ = [ 'MenuBox', ]

class MenuBoxChild( DropDownBoxChild ):

    def handle_ButtonRelease( self, e ):
        if not e.detail == 1:
            self.toggle_hidden()
            
        menu_item = self.get_menu_item( e.event_x, e.event_y )
        self.toggle_hidden()

        self.spawn_process( menu_item['command'] )

    def get_menu_item( self, x, y ):
        per_item_size = self.height / len( self.parent.menu_items )
        item_index = int( math.floor( float( y ) / per_item_size ) )

        return self.parent.menu_items[ item_index ]

    def spawn_process( self, command, **kwargs ):
        subprocess.Popen( command, **kwargs )

class MenuBox( DropDownBox ):

    def __init__( self, title, menu_items, *args, **kwargs ):
        DropDownBox.__init__( self, *args, **kwargs )
        
        self.text = title
        self.menu_items = menu_items

    def _configure( self, qtile, screen ):
        DropDownBox._configure( self, qtile, screen, child_class = MenuBoxChild )

        self.child.text = '\n'.join( list( item['name'] for item in self.menu_items ) )

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
