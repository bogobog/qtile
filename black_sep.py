
from libqtile import widget

__all__ = [ 'BlackSep', ]

class BlackSep( widget.Sep ):
    def __init__( self ):
        super( BlackSep, self ).__init__( foreground = '000000' )

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
