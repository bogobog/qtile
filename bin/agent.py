#!/usr/bin/python

import pyinotify, time
from multiprocessing import Process, Lock, Condition
from libqtile.command import Client, CommandError
from libqtile.ipc import IPCError

WATCHERS_MANIFEST = { 
    'volumetextbox': { 'widget_name': 'VolumeTextBox', 'interval': 0.1, 'update_child': False },
    'timedropdownbox': { 'widget_name': 'TimeDropDownBox', 'interval': 1, 'update_child': False },
    'timedropdownbox_child': { 'widget_name': 'TimeDropDownBox', 'interval': 5, 'update_child': True },
}

class INotifyWatcher( object ):

    WATCHER_TMP_DIR = '/dev/shm'
    WATCHER_TMP_PREFIX = 'qtile'
    QTILE_CLIENT_LOCK = Lock()
    CHECK_LOCK = Condition()

    def __init__( self, watcher_name, widget_name, sleep_interval, update_child ):
        
        self.watcher_name = watcher_name
        self.widget_name = widget_name
        self.sleep_interval = sleep_interval
        self.update_child = update_child

        self.watch_file = "{}/{}_{}".format( self.WATCHER_TMP_DIR, self.WATCHER_TMP_PREFIX, watcher_name )
        self.qtile_client = Client()

    def check( self ):
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier( wm, self.notify_handler, timeout = 10 )

        watch_add = None
        while True:
            self.CHECK_LOCK.acquire()
            self.CHECK_LOCK.wait( self.sleep_interval )

            if not watch_add:
                results = wm.add_watch( self.watch_file, pyinotify.IN_CREATE | pyinotify.IN_MODIFY )
                result_value = results.values()[0]
                if result_value > 0:
                    watch_add = result_value
            else:
                notifier.process_events()
                while notifier.check_events():
                    notifier.read_events()
                    notifier.process_events()

            self.CHECK_LOCK.release() 

    def notify_handler( self, event ):

        global qtile_client

        with file( self.watch_file, 'r' ) as wf:
            file_contents = wf.read().rstrip()

        target_func = ( self.update_child and self.qtile_client.widget[ self.widget_name ].update_child ) or self.qtile_client.widget[ self.widget_name ].update

        try:
            self.QTILE_CLIENT_LOCK.acquire()
            target_func( file_contents )
        except ( IPCError, CommandError ) as e:
            time.sleep( 1 )
            self.QTILE_CLIENT_LOCK.release()
            self.notify_handler( event )
        else:
            self.QTILE_CLIENT_LOCK.release()

if __name__ == '__main__':
    
    from logging import CRITICAL, DEBUG
    import socket
    import sys
    import time
    import os.path
    import signal

    global lock_socket
    lock_socket = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )

    try:
        lock_socket.bind( '\0' + os.path.basename( sys.argv[0] ))
    except socket.error:
        sys.exit()

    pyinotify.log.setLevel( CRITICAL )

    watchers = []

    def term_handler( *args, **kwargs ):
        for proc in watchers:
            proc.terminate()

        time.sleep( 2 )
        sys.exit()

    signal.signal( signal.SIGTERM, term_handler )
    signal.signal( signal.SIGINT, term_handler )

    for name, values in WATCHERS_MANIFEST.items():
        watcher = INotifyWatcher( name, values['widget_name'], values['interval'], values['update_child'] )
        new_process = Process( target = watcher.check )
        new_process.daemon = True
        new_process.start()
        watchers.append( new_process )

    for proc in watchers:
        proc.join()

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab
