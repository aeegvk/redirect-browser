import os
import json
import webbrowser

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
    parts = link.split("://")
    if len(parts) != 2:
        print("Invalid link format")
        return
    
    domain = parts[1]
    browser_cmd = browser_mapping.get(domain, "xdg-open")
    
    try:
        webbrowser.get(browser_cmd).open(link)
    except webbrowser.Error:
        print(f"Error opening link with {browser_cmd}")
        try:
            webbrowser.open(link)  # Try system default browser
        except webbrowser.Error:
            print("Error opening link with system default browser")

if __name__ == "__main__":
    if len(os.sys.argv) != 2:
        print("Usage: python link_redirector.py <url>")
        os.sys.exit(1)
    
    link = os.sys.argv[1]
    open_link(link)
