
from libqtile import widget

class Volume(widget.Volume):

    def __init__(self, *args, **kwargs):
        widget.Volume.__init__(self, *args, **kwargs)
        self.markup = True

    def update(self, *args, **kwargs):
        widget.Volume.update(self, *args, **kwargs)

        if self.text == 'M':
            self.text = '<span bgcolor="red"> M </span>'
        else:
            self.text = self.text.rstrip('%').center( 3 )

