#!C:\Python27\python.exe

import os, sys, codecs, string, glob
import plasTeX
from plasTeX.TeX import TeX
from plasTeX.Config import config
from plasTeX.ConfigManager import *
from plasTeX.Logging import getLogger

log = getLogger()

__version__ = '0.9.1'

def main(argv):
    """ Main program routine """
    print >>sys.stderr, 'plasTeX version %s' % __version__

    # Parse the command line options
    try: 
        opts, args = config.getopt(argv[1:])
    except Exception, msg:
        log.error(msg)
        print >>sys.stderr, config.usage()
        sys.exit(1)

    if not args:
        print >>sys.stderr, config.usage()
        sys.exit(1)

    file = args.pop(0)

    # Create document instance that output will be put into
    document = plasTeX.TeXDocument(config=config)

    # Instantiate the TeX processor and parse the document
    tex = TeX(document, file=file)

    # Populate variables for use later
    if config['document']['title']:
        document.userdata['title'] = config['document']['title']
    jobname = document.userdata['jobname'] = tex.jobname
    cwd = document.userdata['working-dir'] = os.getcwd()

    # Load aux files for cross-document references
    pauxname = '%s.paux' % jobname
    rname = config['general']['renderer']
    for dirname in [cwd] + config['general']['paux-dirs']:
        for fname in glob.glob(os.path.join(dirname, '*.paux')):
            if os.path.basename(fname) == pauxname:
                continue
            document.context.restore(fname, rname)

    # Parse the document
    tex.parse()

    # Set up TEXINPUTS to include the current directory for the renderer
    os.environ['TEXINPUTS'] = '%s:%s' % (os.getcwd(), 
                                         os.environ.get('TEXINPUTS',''))

    # Change to specified directory to output to
    outdir = config['files']['directory']
    if outdir:
        outdir = string.Template(outdir).substitute({'jobname':jobname})
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        log.info('Directing output files to directory: %s.' % outdir)        
        os.chdir(outdir)
    
    # Load renderer
    try: 
        exec('from plasTeX.Renderers.%s import Renderer' % rname)
    except ImportError, msg:
        log.error('Could not import renderer "%s".  Make sure that it is installed correctly, and can be imported by Python.' % rname)
        sys.exit(1)

    # Write expanded source file
    #sourcefile = '%s.source' % jobname
    #open(sourcefile,'w').write(document.source.encode('utf-8'))
    
    # Write XML dump
    #outfile = '%s.xml' % jobname
    #open(outfile,'w').write(document.toXML().encode('utf-8'))
    
    # Apply renderer
    Renderer().render(document)

    print

def info(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      # we are in interactive mode or we don't have a tty-like
      # device, so we call the default hook
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      # we are NOT in interactive mode, print the exception...
      traceback.print_exception(type, value, tb)
      print
      # ...then start the debugger in post-mortem mode.
      pdb.pm()

#sys.excepthook = info

#sys.setrecursionlimit(10000)
    
#main(sys.argv)
try:
    main(sys.argv)
except KeyboardInterrupt:
    pass
