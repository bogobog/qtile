
import os
from libqtile.widget import base

class MarkupThreadedPollText( base.ThreadedPollText ):

    def __init__( self, *args, **kwargs ):
        base.ThreadedPollText.__init__( self, *args, **kwargs )
        self.markup = True

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
