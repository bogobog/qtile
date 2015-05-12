
from libqtile.widget import TextBox

__all__ = [ 'MarkupTextBox', ]

class MarkupTextBox( TextBox ):

    def __init__( self, *args, **kwargs ):
        TextBox.__init__( self, *args, **kwargs )
        self.markup = True    
    
# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
