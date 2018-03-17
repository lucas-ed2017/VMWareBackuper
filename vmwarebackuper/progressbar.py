class progressbar:

    def __init__(self, progress, total):
        self.progress = progress
        self.total = total

    def update_progress(self, progress):
        barLength = 50
        status = ""
        self.progress += progress
        if isinstance(progress, int):
            self.progress = float(progress)
        elif not isinstance(progress, float):
            self.progress = 0
            status = "error: progress var must be float\r\n"

        if progress < 0:
            self.progress = 0
            status = "Halt...\r\n"
        elif progress >= 1:
            self.progress = 1
            status = "Done...\r\n"

        block = int(round(barLength*self.progress))
        text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength - block), round(self.progress*100, 2), status)
        print('\r' + (text), end="")
