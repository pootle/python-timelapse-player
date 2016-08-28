#!/usr/bin/python3

import os, time, sys
from pathlib import Path
import http.server
from urllib.parse import urlparse, parse_qs
from socketserver import ThreadingMixIn
import threading
import argparse

class camhandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        pr = urlparse(self.path)
        if pr.path.endswith('.jpg'):
            lnames=pr.path.split('/')
            finalname=lnames[-1]
            ty = finalname.split('.')
            if len(ty[-2]) == 0:
                ino=0
            else:
                ino = int(ty[-2])
            ifile = filesdir / sorted_files[ino]
            self.servefile(ifile,'image/jpeg')
            return

        pf = pr.path.split('/')
        if pf[-1] == '' or pf[-1] == 'index.html':
            sfp = Path('index.html')
            with sfp.open('rb') as sfile:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(sfile.read().replace(b'{$x$}',str(len(sorted_files)-1).encode('utf-8')))
        else:
            self.send_error(404,"I think there may be an error - I only do jpegs")
            return

    def servefile(self,sfp,ctype):
        self.send_response(200)
        self.send_header('Content-type',ctype + '; charset=utf-8')
        self.end_headers()
        with sfp.open('rb') as sfile:                
            self.wfile.write(sfile.read())

    def log_message(self, format, *args):
        return

class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""

DEFBASEDIR = '/home/iain/Desktop/jigsawtl/day2/cl'
DEFWEBPORT = 8090

if __name__ == '__main__':
    global filesdir
    global sorted_files
    try:
        assert sys.version_info > (3,4)
    except:
        print("I'm sorry Dave, I can't do this with python < 3.5")
        sys.exit(-1)
    
    parser = argparse.ArgumentParser()
    parser.add_argument( "-w", "--webport", type=int
        , help="port used for the webserver, default %d" % DEFWEBPORT)
    parser.add_argument( "-d", "--basedir"
        , help="base directory for web server, default %s" % DEFBASEDIR)
    parser.add_argument("-s", "--stereo", action="store_true"
        , help="expect left / right stereo images in cl / cr directories")

    args = parser.parse_args()
    webport = args.webport if args.webport else DEFWEBPORT
    basedir = Path(args.basedir if args.basedir else DEFBASEDIR)
    do3d = args.stereo

    flist = [x for x in ((basedir / 'cl') if do3d else basedir).iterdir() if x.is_file()]
    sorted_files = sorted(flist, key=lambda x: x.stem)
    print("starting server with %d files from %s on port %d ." %(len(sorted_files), basedir.__str__(), webport))
    filesdir = basedir
    try:
        server = ThreadedHTTPServer(('',webport),camhandler)
        print("server started with %d files" % len(sorted_files))
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
