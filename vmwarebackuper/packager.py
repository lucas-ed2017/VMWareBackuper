#!/bin/python
# -*- coding: utf-8 -*-

import shutil
from os import stat
import progressbar

class packager:
    def __init__(self, path, finalfile):
        self.path = path
        self.finalfile = finalfile
        
    def compress(self):
        total = stat(self.path).st_size
        bar = progressbar.progressbar(0, total)
        cb = create_callback(bar, total)
        shutil.make_archive(self.path, 'tar.gz', self.finalfile, callback=cb)
        
        def create_callback(progressbar, total):  # os underlines no nome da funcao tornam ela 'private', o que dificulta a utilizacao em outras classes
            def cb(data):
                progressbar.update_progress(len(data))
            return cb
