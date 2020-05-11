
verbose = False
debug = False

def set(args=None):
    global verbose, debug
    if args is None:
        return
    if 'debug' in args:
        debug = args['debug']
    if 'verbose' in args:
        verbose = args['verbose'] or debug

def dump():
    print("verbose: ", verbose)
    print("debug: ", debug)
