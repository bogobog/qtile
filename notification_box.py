
import math

from libqtile.notify import notifier
from multiprocessing import Lock

from .drop_down_box import DropDownBox, DropDownBoxChild

__all__ = [ 'NotificationBox', ]

class NotificationBoxChild( DropDownBoxChild ):

    @classmethod
    def getFormattedContent( klass, notifications ):
        new_text_array = []
        for item in notifications:
            new_text = item.summary.encode('ascii', 'ignore')
            if not new_text[-1] == ':':
                new_text += ":"

            new_text += " %s" % item.body.encode('ascii', 'ignore')

            new_text_array.append( new_text )

        return '\n'.join( new_text_array )
        
class NotificationBox( DropDownBox ):

    NO_NOTIFICATIONS_MSG = 'No notifications'

    def __init__( self, *args, **kwargs ):
        DropDownBox.__init__( self, *args, **kwargs )
        
        self.text = ' 0 '

        self.notifications = list()
        self.queue_update_lock = Lock()

        notifier.register( self.add_notification )

    def _configure( self, qtile, screen ):
        DropDownBox._configure( self, qtile, screen, child_class = NotificationBoxChild )

        self.child.text = self.NO_NOTIFICATIONS_MSG

    def add_notification( self, notification ):

        with self.queue_update_lock:
            self.notifications.append( notification )
            self.child.text = NotificationBoxChild.getFormattedContent( self.notifications )
            self.update( '<span bgcolor="red"> %d </span>' % len( self.notifications ) )

    def button_release( self, x, y, button ):

        if button == 3:
            self.notifications = list()
            self.child.window.hide()
            self.child.text = self.NO_NOTIFICATIONS_MSG
        else:
            DropDownBox.button_release( self, x, y, button )

        self.update( ' %d ' % len( self.notifications ) )

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
