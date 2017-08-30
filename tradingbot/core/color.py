# CONSTANTS
CYAN = '\033[96m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
WHITE = '\033[0m'
MAGENTA = '\033[35m'
BOLD = '\033[01m'
UNDERLINE = '\033[04m'


# COLOR FUNCTIONS
def bold(str):
    return BOLD + str + WHITE
def underline(str):
    return UNDERLINE + str + WHITE
def cyan(str):
    return CYAN + str + WHITE
def purple(str):
    return PURPLE + str + WHITE
def blue(str):
    return BLUE + str + WHITE
def green(str):
    return GREEN + str + WHITE
def red(str):
    return RED + str + WHITE
def yellow(str):
    return YELLOW + str + WHITE
def white(str):
    return WHITE + str + WHITE

class printer(object):
    @staticmethod
    def header(string):
        return bold(blue('------ ' + str(string.upper()) + ' ------'))

    @staticmethod
    def process(string=''):
        return '[' + cyan('+') + '] ' + str(string)

    @staticmethod
    def info(string=''):
        return '[' + blue('#') + '] ' + str(string)

    @staticmethod
    def warning(string=''):
        return '[' + yellow('-') + '] ' + str(string)

    @staticmethod
    def error(string=''):
        return '[' + magenta('=') + '] ' + str(string)

    @staticmethod    
    def critical(string=''):
        return '[' + red('~') + '] ' + str(string)

    @staticmethod
    def user_input(string=''):
        return '[' + green('$') + '] ' + str(string)