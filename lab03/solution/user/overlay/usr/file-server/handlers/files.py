import os
import tornado.web
from file_tree import build_file_tree
from routes import Routes, Templates
from .base import BaseHandler

BASE = os.path.dirname(__file__)
FILE_DIRECTORY = os.path.abspath(os.path.join(BASE, "..", "files"))

class FileListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        tree = build_file_tree(FILE_DIRECTORY)
        self.render(Templates.index, tree=tree)

class FileDownloadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        filename = self.get_argument("filename", None)
        if not filename:
            self.write("Filename parameter is missing.")
            return

        file_path = os.path.join(FILE_DIRECTORY, filename)
        full_path = os.path.abspath(file_path)
        allowed_path = os.path.abspath(FILE_DIRECTORY)

        if not full_path.startswith(allowed_path):
            self.set_status(403)
            self.write("Access denied.")
            return

        if not os.path.exists(full_path) or os.path.isdir(full_path):
            self.set_status(404)
            self.write("File not found.")
            return

        self.set_header("Content-Type", "application/octet-stream")
        safe_filename = os.path.basename(filename)
        self.set_header("Content-Disposition", f"attachment; filename={safe_filename}")
        with open(full_path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)
                self.flush()
        self.finish()        

class FileUploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        if "file" not in self.request.files:
            self.write("No file part in the request.")
            return

        fileinfo = self.request.files["file"][0]
        filename = fileinfo["filename"]
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(FILE_DIRECTORY, safe_filename)

        with open(file_path, "wb") as f:
            f.write(fileinfo["body"])

        self.write(f"File '{safe_filename}' uploaded successfully. <a href='{Routes.files}'>Back to file tree</a>.")