import sys, os, tty
import select

def kbhit(timeout=0.001):
    fd = sys.stdin.fileno()
    ttyMode = tty.tcgetattr(fd)
    tty.setcbreak(fd)
    try:
        result = bool(select.select([sys.stdin], [], [], timeout)[0])
    finally:
        #tty.tcsetattr(fd, tty.TCSAFLUSH, ttyMode)
        tty.tcsetattr(fd, tty.TCSANOW, ttyMode)
    return result

if __name__ == "__main__":
    while 1:
        if kbhit(0.1):
             print "What do you have to say to me? ",
             print sys.stdin.readline()
             print
    print "bye!"
