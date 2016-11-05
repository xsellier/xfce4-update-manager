#!/usr/bin/env python

import notify2
import subprocess
import sys, os
import signal
import aptmanager
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import fcntl, sys

scriptDirectory = os.path.abspath(os.path.dirname(__file__))
pid_file = '{0}/update-manager.pid'.format(scriptDirectory)

fp = open(pid_file, 'w')

try:
  fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
  # another instance is running
  sys.exit(0)

# Ubuntu's notify-osd doesn't officially support actions. However, it does have
# a dialog fallback which we can use for this demonstration. In real use, please
# respect the capabilities the notification server reports!
OVERRIDE_NO_ACTIONS = True

def exec(command):
  Gtk.main_quit()

  try:
    process = subprocess.Popen(command)

    process.wait()

    if process.returncode == 0:
      # Image URI
      icon = "file://{0}/icons/icon-ok.png".format(scriptDirectory)

      notifyResult(icon, 'Your system is up-to-date !')
    else:
      # Image URI
      icon = "file://{0}/icons/icon-fail.png".format(scriptDirectory)

      notifyResult(icon, 'Update failed !')
  except subprocess.CalledProcessError as err:
    # Image URI
    icon = "file://{0}/icons/icon-fail.png".format(scriptDirectory)

    notifyResult(icon, 'Error during update: {0}'.format(err))

def performUpdate(notification=None, signal_text=None):
  # Perform an apt update, then an apt upgrade, if the ugprade fails, it performs an install
  exec(['gksudo', '{0}/scripts/update.sh'.format(scriptDirectory)])

def update(notification, signal_text):
  close(notification, signal_text)
  performUpdate()

def notifyResult(icon, message):
  notification = notify2.Notification("Package updater", message, icon)

  notification.show()

def close(notification, signal_text=None):
  notification.close()

def updateFromTray(notification):
  def performUpdateFromTray(status):
    status.set_visible(False)
    notification.close()
    performUpdate()

  return performUpdateFromTray

if __name__ == '__main__':
  pkgs = aptmanager.get_update_packages()

  if pkgs:
    notify2.init("Package updater", mainloop='glib')

    # Image URI
    icon = "file://{0}/icons/icon-info.png".format(scriptDirectory)

    notification = notify2.Notification("Package updater", "Updates are available", icon)
    notification.add_action("update", "Apply update", update)
    notification.add_action("cancel", "Not now !", close)

    notification.connect("closed", close)

    # Ignore SIGINT signal otherwise loop hangs
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    if not notification.show():
      print("Failed to send notification")
    else:
      status = Gtk.StatusIcon()

      iconFile = "{0}/icons/icon-update.png".format(scriptDirectory)

      status.set_from_file(iconFile)
      status.set_visible(True)
      status.connect('popup-menu', updateFromTray(notification))
      status.connect('activate', updateFromTray(notification))

      Gtk.main()
