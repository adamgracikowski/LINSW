#!/usr/bin/python3

import os
import sys
import signal
import asyncio
import tornado.web

from handlers.base import ItemsModule
from handlers.auth import LoginHandler, LogoutHandler
from handlers.files import FileListHandler, FileUploadHandler, FileDownloadHandler

from routes import Routes

BASE = os.path.dirname(__file__)
TEMPLATES = os.path.join(BASE, "templates")
FILE_DIRECTORY = os.path.join(BASE, "files") # '/mnt' in the future

def make_app():
    return tornado.web.Application(
        [
            (Routes.login, LoginHandler),
            (Routes.logout, LogoutHandler),
            (Routes.files, FileListHandler),
            (Routes.download, FileDownloadHandler),
            (Routes.upload, FileUploadHandler),
        ],
        cookie_secret="__SECRET_KEY__",
        login_url=Routes.login,
        template_path=TEMPLATES,
        ui_modules={"items": ItemsModule},
        debug=True
    )

async def main():
    os.makedirs(FILE_DIRECTORY, exist_ok=True)

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    address = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

    app = make_app()
    app.listen(port=port, address=address)

    print(f"Server is running on http://{address}:{port}")

    shutdown_event = asyncio.Event()

    def handle_signal():
        print("\nShutting down...")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGTERM, handle_signal)

    await shutdown_event.wait()

    print("Server stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass