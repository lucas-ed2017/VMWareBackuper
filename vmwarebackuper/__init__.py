try:
    #importacao a la python3
    from vmwarebackuper.vmwarebackuper import vmwarebackuper
    from vmwarebackuper.ftpserver import ftpserver
    from vmwarebackuper.packager import packager
    from vmwarebackuper.virtualmachine import virtualmachine
except ImportError:
    #se a importacao der erro, facamos uma que funcione no python2
    from vmwarebackuper import vmwarebackuper
    from ftpserver import ftpserver
    from packager import packager
    from virtualmachine import virtualmachine
