
verbose = False
debug = False

def set(args=None):
    global verbose, debug
    if args is None:
        return
    debug = args['debug']
    verbose = args['verbose'] or debug

def dump():
    print("verbose: ", verbose)
    print("debug: ", debug)
