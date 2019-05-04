#!/bin/python
# -*- coding: utf-8 -*-
#code from: https://mail.python.org/pipermail/python-list/2010-July/581965.html

import sys
import os
import tarfile
import progressbar

class packager:
    def __init__(self, src_folder, dest_folder, extension='.tar.gz', path='/vmfs/volumes/datastore1/', bar=True):
        self.src_folder = src_folder
        self.dest_folder = dest_folder
        self.extension = extension
        self.path = path
        self.bar = bar
        
    def compress(self):
        if self.bar:
            tar = mytarfile.open(self.dest_folder + self.extension, "w:gz", callback=callback)
        else:
            tar = mytarfile.open(self.dest_folder + self.extension, "w:gz", callback = None)
        tar.add(self.path + self.src_folder)
        tar.close()


class fileproxy(object):
    def __init__(self, fobj, callback):
        self.fobj = fobj
        self.callback = callback
        self.size = os.fstat(self.fobj.fileno()).st_size

    def read(self, size):
        self.callback(self.fobj.tell(), self.size)
        return self.fobj.read(size)

    def close(self):
        self.callback(self.size, self.size)
        self.fobj.close()


class mytarfile(tarfile.TarFile):

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("callback")
        super(mytarfile, self).__init__(*args, **kwargs)

    def addfile(self, tarinfo, fileobj=None):
        if self.callback is not None and fileobj is not None:
            fileobj = fileproxy(fileobj, self.callback)
        super(mytarfile, self).addfile(tarinfo, fileobj)


def callback(processed, total):
    #sys.stderr.write("%.1f%% \r" % (processed / float(total) * 100))
    bar = progressbar.progressbar(0, total)
    bar.update_progress(processed)


