
import os

from .markup_threaded_poll_text import MarkupThreadedPollText

class LoadAverageBox( MarkupThreadedPollText ):

    defaults = [
        ("update_interval", 5, "Update interval in seconds, if none, the "
            "widget updates whenever the event loop is idle."),
    ]

    def __init__( self, *args, **kwargs ):
        MarkupThreadedPollText.__init__( self, *args, **kwargs )
        self.add_defaults( LoadAverageBox.defaults )

    def poll( self ):
        return "%.2f %.2f %.2f" % os.getloadavg()

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
