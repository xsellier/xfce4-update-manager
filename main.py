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


scriptDirectory = os.path.abspath(os.path.dirname(__file__))

# Ubuntu's notify-osd doesn't officially support actions. However, it does have
# a dialog fallback which we can use for this demonstration. In real use, please
# respect the capabilities the notification server reports!
OVERRIDE_NO_ACTIONS = True

def exec(command):

  try:
    process = subprocess.Popen(command,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
    )

    process.wait()

    output = process.stdout.readline().strip().decode('utf8')
    error = process.stderr.readline().strip().decode('utf8')

    if process.returncode == 0:
      # Image URI
      icon = "file://{0}/icons/icon-ok.png".format(scriptDirectory)

      notifyResult(icon, 'Your system is up-to-date !')
    else:
      # Image URI
      icon = "file://{0}/icons/icon-fail.png".format(scriptDirectory)

      notifyResult(icon, 'Update failed !\n{0}\n{1}'.format(output, error))
  except subprocess.CalledProcessError as err:
    # Image URI
    icon = "file://{0}/icons/icon-fail.png".format(scriptDirectory)

    notifyResult(icon, 'Error during update: {0}'.format(err))

def update(notification, signal_text):
  close(notification, signal_text)

  # Perform an apt update, then an apt upgrade, if the ugprade fails, it performs an install
  exec(['gksudo', '{0}/scripts/update.sh'.format(scriptDirectory)])

def notifyResult(icon, message):
  notification = notify2.Notification("Package updater", message, icon)

  notification.show()

def close(notification, signal_text=None):
  Gtk.main_quit()
  notification.close()

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
      Gtk.main()
