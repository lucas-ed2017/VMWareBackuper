import shutil
from os import stat
import progressbar


def create_callback( progressbar, total):  # os underlines no nome da funcao tornam ela 'private', o que dificulta a utilizacao em outras classes
    def cb(data):
        progressbar.update_progress(len(data))

    return cb

file = 'soul_eater'

total = stat(file).st_size
bar = progressbar.progressbar(0, total)
cb = create_callback(bar, total)

shutil.make_archive('soul_eater2', 'zip', 'soul_eater', callback=cb)

