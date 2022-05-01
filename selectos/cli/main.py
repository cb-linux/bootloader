import sys
from subprocess import call as cmd
import subprocess
import pytermgui as ptg
import functools

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

def returnToMenu():
    container = menuContainer

def viewDmesg():
    # Provides a color output of dmesg with less
    subprocess.run(['dmesg', '--human', '--color=always'])

def viewMoreInformation():
    # inxi,
    pass

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
        ["More information", lambda *_: manager.exit()],
        "",
        "[wm-title bold] Exit",
        "",
        ["Shutdown", lambda *_: powerOff()],
        ["Reboot", lambda *_: reboot()],
        ""
    )

    # Make the container a global so we can modify it from other functions
    global container
    container = menuContainer

    # Decrease width to half of the terminal screen
    container.relative_width = 0.5

    window = ptg.Window(container)

    # Disable border
    window.styles.border = '0'

    window.toggle_fullscreen()

    manager.add(window)
    manager.run()