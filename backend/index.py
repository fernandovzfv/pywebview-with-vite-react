import os
from time import time
from datetime import datetime

import webview
from tools import set_interval

from api import (
    join_tables,
    get_row_by_id,
    filter_data,
)
from api import FIELDS_TO_SHOW


class Api:
    def __init__(self):
        self.data = join_tables("database.db", "table1", "table2", "id")
        # print(f"CWD: {os.getcwd()}")
        # print(self.data[0])

    def execute_command(self, command):
        """
        Execute a given command and return the corresponding data or result.

        This function interprets various commands related to document tracking management,
        such as retrieving all data, searching by ID, checking delays in revisions,
        filtering by status, and identifying documents with delays in review or update.

        Parameters:
        command (str): A string representing the command to be executed.
                       Supported commands include:
                       - "/all": Retrieve all data
                       - "/id <value>": Search for a specific ID

        Returns:
        Various: The return type depends on the command executed:
                 - For "/all": Returns the entire DATA set
                 - For "/id": Returns a specific row from DATA
        """
        if command == "/all":
            return filter_data(self.data, FIELDS_TO_SHOW)
        elif command.startswith("/id "):
            value_to_search = command.split()[1]
            return get_row_by_id(self.data, value_to_search)
        else:
            return [{"error": "Invalid command"}]

    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, "w") as f:
            f.write(content)

    def ls(self):
        return os.listdir(".")


def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists("../gui/index.html"):  # unfrozen development
        return "../gui/index.html"

    if exists("../Resources/gui/index.html"):  # frozen py2app
        return "../Resources/gui/index.html"

    if exists("./gui/index.html"):
        return "./gui/index.html"

    raise Exception("No index.html found")


entry = get_entrypoint()


@set_interval(1)
def update_ticker():
    if len(webview.windows) > 0:
        webview.windows[0].evaluate_js(
            'window.pywebview.state.setTicker("%s")'
            % datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == "__main__":
    window = webview.create_window("pywebview", entry, js_api=Api())
    webview.start(update_ticker, debug=True)
