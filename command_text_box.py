
from .markup_text_box import MarkupTextBox

__all__ = [ 'CommandTextBox', ]

class CommandTextBox( MarkupTextBox ):

    def __init__( self, command, *args, **kwargs ):
        MarkupTextBox.__init__( self, *args, **kwargs )
        self.button_command = command
    
    def button_release( self, x, y, button ):
        self.qtile.cmd_spawn( self.button_command )

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
