#! /usr/bin/env python3

import os
import json
import subprocess
from tldextract import extract

def load_config(filename):
    with open(filename, "r") as config_file:
        return json.load(config_file)

config = load_config("config.json")

browser_mapping = config["browser_mapping"]

def set_default_browser(browser_name):
    mime_apps_file = os.path.expanduser("~/.config/mimeapps.list")
    with open(mime_apps_file, "a") as f:
        f.write(f"xdg-settings set default-web-browser {browser_name}\n")


def register_protocol_handler(protocol, app_name):
    mime_apps_file = os.path.expanduser("~/.config/mimeapps.list")
    with open(mime_apps_file, "a") as f:
        f.write(f"x-scheme-handler/{protocol}={app_name}.desktop;\n")


def open_link(link):
    extracted_domain = extract(link)
    domain = extracted_domain.registered_domain
    browser_cmd = browser_mapping.get(domain, "firefox")
    cmd = [browser_cmd, link]

    try:
        status = subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        print(f"Error opening link with {browser_cmd}")
        try:
            status = subprocess.check_call(['firefox', link])  # Try system default browser
        except subprocess.CalledProcessError:
            print("Error opening link with system default browser")

if __name__ == "__main__":
    if len(os.sys.argv) != 2:
        print("Usage: python link_redirector.py <url>")
        os.sys.exit(1)

    link = os.sys.argv[1]
    open_link(link)
