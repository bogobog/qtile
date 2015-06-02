
from libqtile.window import Window, Internal
from libqtile.drawer import Drawer
from libqtile.command import CommandObject
from libqtile.configurable import Configurable
from libqtile.pangocffi import pango

from xcffib.xproto import EventMask
from HTMLParser import HTMLParser

from .markup_text_box import MarkupTextBox

__all__ = [ 'DropDownBox', ]

def strip_markup( text ):

    class MLStripper( HTMLParser ):
        def __init__( self ):
            self.reset()
            self.fed = []
        def handle_data( self, d ):
            self.fed.append(d)
        def get_data( self ):
            return ''.join( self.fed )

    s = MLStripper()
    s.feed( text )
    return s.get_data()

class DropDownBoxChild( CommandObject ):

    X_PADDING = 2

    def __init__( self, parent, background = "#737373", opacity = 1 ):
        CommandObject.__init__( self )

        self.name = self.__class__.__name__.lower()

        self.parent = parent
        self.background = background
        self.opacity = opacity

        self._text = ""
        self._width = 1 + ( self.X_PADDING * 2 )
        self._height = 1

        self.configured = False

    def _configure( self, qtile, screen ):
        self.qtile = qtile
        self.screen = screen

        self.window = Internal.create( self.qtile, self.x, self.y, self.width, self.height, self.opacity )
        self.window.handle_Expose = self.handle_Expose
        self.window.handle_ButtonRelease = self.handle_ButtonRelease
        self.qtile.windowMap[ self.window.window.wid ] = self.window

        self.generateDrawer()

        self.configured = True

    def generateDrawer( self ):
        self.window.x = self.x
        self.window.y = self.y
        self.window.width = self.width
        self.window.height = self.height

        self.drawer = Drawer( self.qtile, self.window.window.wid, self.width, self.height )
        self.layout = self.drawer.textlayout( self._text, self.parent.foreground, self.parent.font, self.parent.fontsize, None, markup = True )
        self.layout.layout.set_alignment( pango.PANGO_ALIGN_LEFT )

        self.frame = self.layout.framed( 0, self.parent.bar.background, self.X_PADDING, 0 )

        self.draw()
    
    @property
    def x( self ):
        # parent has yet to be configured
        if self.parent.offset == None:
            return 0

        # if width equals parent width, return parent offset
        # if width is less than parents width, return parent offset
        # if width is greater than screen length, return parent offset
        if self.width <= self.parent.width or self.width >= self.parent.bar.screen.width:
            return self.parent.offset

        # if width is greater than parents width
        if self.width > self.parent.width:
            # if parent offset plus width is greater then remaining screen length, return screen length minus width
            if ( self.width + self.parent.offset ) > ( self.parent.bar.screen.width - self.parent.offset ):
                return self.parent.bar.screen.width - self.width
            # if parent offset plus width is less than screen length, return parent offset
            else:
                return self.parent.offsetx

        # "shouldnt" get here
        return 0

    @x.setter
    def x( self, value ):
        return

    @property
    def y( self ):
        return self.parent.height

    @y.setter
    def y( self, value ):
        return
        
    @property
    def text( self ):
        return self._text

    @text.setter
    def text( self, value ):

        self._text = value

        if self.configured:
            width, height = self.drawer.max_layout_size( [ strip_markup( self._text ), ], self.parent.font, self.parent.fontsize )
            self._width = width + ( self.X_PADDING * 2 )
            self._height = height

            self.generateDrawer()

    @property
    def width( self ):
        return max( [ self._width, self.parent.width ] )

    @width.setter
    def width( self, value ):
        return 

    @property
    def height( self ):
        return self._height

    @height.setter
    def height( self, value ):
        return

    def draw( self ):
        if not self.configured:
            return

        self.window.place( 
            self.screen.x + self.x,
            self.y,
            self.width,
            self.height,
            0, 
            None, 
            above = True 
        )

        self.drawer.clear( self.background )
        self.frame.draw( 0, 0 )
        self.drawer.draw( width = self.width )

    def info(self):
        if not self.configured:
            return 

        return dict( width = self.parent.width, height = self.parent.height, window = self.window.window.wid )

    def toggle_hidden( self ):
        if not self.configured:
            return

        if self.window.hidden:
            self.window.unhide()
        else:
            self.window.hide()

    def handle_Expose( self, e ):
        self.draw()

    def handle_ButtonRelease( self, e ):
        self.toggle_hidden()

class DropDownBox( MarkupTextBox ):

    defaults = [
        ("child_text", '', "Child window contents."),
    ]

    def __init__( self, *args, **kwargs ):

        MarkupTextBox.__init__( self, *args, **kwargs )
        self.add_defaults( DropDownBox.defaults )

        self.configured = False

    def button_release( self, x, y, button ):
        self.child.toggle_hidden()

    def _configure( self, qtile, screen, child_class = DropDownBoxChild ):
        MarkupTextBox._configure( self, qtile, screen )
        self.qtile = qtile
        self.screen = screen

        self.child = child_class( self )
        self.child._configure( self.qtile, self.screen )
        self.child.text = self.child_text

        self.configured = True

    def draw( self ):
        if self.offsetx == None or not self.configured:
            return

        self.child.draw()

        return MarkupTextBox.draw( self )

    def cmd_update( self, text ):
        MarkupTextBox.cmd_update( self, text )
        self.child.generateDrawer()

    def cmd_update_child( self, text ):
        self.child.text = text

    def cmd_get_child( self ):
        return self.child.text

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
