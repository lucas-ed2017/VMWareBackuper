class progressbar:

    def __init__(self, progress, total, barlength = None):
        self.progress = float(progress)
        self.total = float(total)

        try:
            import console
            if barlength == None: #verifica se o tamanho da barlength eh o padrao
                (self.barlength, throwaway) = console.getTerminalSize() #se eh o tamanho padrao tenta pegar o tamanho do console e usa-lo
        except ImportError: #se a importacao de console der errado, usar 50 como tamanho padrao da barlength
            if barlength == None: #verifica se o tamanho da barlength eh o padrao
                self.barlength = 50
            

    def update_progress(self, progress):
        barLength = self.barlength
        status = ""
        self.progress += progress

        progress = self.progress/self.total
        
        if isinstance(progress, int):
            progress = float(progress)
        elif not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r"

        

        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        elif progress >= 1:
            progress = 1
            status = "Done...\r\n"

        block = int(round(barLength*progress))
        text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength - block), round(progress*100, 2), status)
        print('\r' + (text), end="") #este eh o modo de printar no python3
        #este eh o modo de printar no python2
        #print '\r' + (text),
