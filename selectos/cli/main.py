import sys
from subprocess import call as cmd
import subprocess
from typing import Container
import pytermgui as ptg
from pytermgui import ansi_interface as ansi
from pytermgui import colors as rgb
import functools
from time import sleep

container = ptg.Container()
window = ptg.Window()
manager = ptg.WindowManager()

# Meant to be used as a decorator:
# @exitIfDev
# def IDontWantToRunThisOnMyDevelopmentMachine():
def exitIfDev(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if len(sys.argv) >= 2:
            return
        return func(*args, **kwargs)
    return inner

def dropToConsole():
    # If this is invoked using fbterm, we can just kill fbterm and drop into a TTY
    # Invocation:
    # sudo fbterm -- python3 main.py
    cmd(["pkill", "fbterm"])


def viewDmesg():
    # Provides a color output of dmesg with less
    cmd(['dmesg', '--human', '--color=always'])

def viewMoreInformation():
    print("The output of quite a few system information commands will be displayed.")
    print("If you want to go to the next one, press q")
    sleep(5)

    # inxi
    print("Inxi:")
    sleep(2)
    cmd(['inxi -FxxxaY -2 | less -R'], shell=True)

    # lshw
    ansi.clear('screen')
    print("Lshw: (may not show all devices due to a minimal kernel being used)")
    sleep(2)
    cmd(['lshw | less -R'], shell=True)

    # lsusb
    ansi.clear('screen')
    print("Lsusb: (may not show all devices due to a minimal kernel being used)")
    sleep(2)
    cmd(['lsusb -v | less -R'], shell=True)

    # lspci
    ansi.clear('screen')
    print("Lspci: (may not show all devices due to a minimal kernel being used)")
    sleep(2)
    cmd(['lspci -vvv | less -R'], shell=True)

    # lsblk
    ansi.clear('screen')
    print("Lsblk: (may not show all devices due to a minimal kernel being used)")
    sleep(2)
    cmd(['lsblk | less -R'], shell=True)

@exitIfDev
def powerOff():
    # Systemctl poweroff depends on Systemd, which often isn't present on embedded
    # poweroff is available on consumer Linux and busybox
    cmd(["poweroff"])

@exitIfDev
def reboot():
    # Universally accepted
    cmd(["reboot"])

with ptg.WindowManager() as manager:

    # BORDER = ptg.boxes.Box([
    #     "╔═════╗",
    #     "║  x  ║",
    #     "╚═════╝",
    # ])

    # BORDER.set_chars_of(ptg.Container)
    ptg.boxes.EMPTY.set_chars_of(ptg.Container)

    # This is our main menu container
    global menuContainer
    menuContainer = ptg.Container(
        "",
        "[wm-title bold]﯀ Select an Operating System",
        "",
        ["Ubuntu", lambda *_: manager.exit()],
        ["Fedora", lambda *_: manager.exit()],
        "",
        "[wm-title bold]ﲉ About",
        "",
        ["Console", lambda *_: dropToConsole()],
        ["View Dmesg", lambda *_: viewDmesg()],
        ["More information", lambda *_: viewMoreInformation()],
        "",
        "[wm-title bold] Exit",
        "",
        ["Shutdown", lambda *_: powerOff()],
        ["Reboot", lambda *_: reboot()],
        ""
    )

    # Make the container a global so we can modify it from other functions
    container = menuContainer

    # Decrease width to half of the terminal screen
    container.relative_width = 0.5

    window = ptg.Window(container)

    # Disable border
    window.styles.border = '0'

    window.toggle_fullscreen()

    manager.add(window)
    manager.run()