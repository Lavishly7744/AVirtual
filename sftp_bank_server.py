import paramiko
import os
from paramiko import SFTPServerInterface, SFTPAttributes, SFTPHandle, SFTP_OK
from socketserver import TCPServer, StreamRequestHandler

class FakeSFTPServer(SFTPServerInterface):
    ROOT = "settlement_files/"

    def list_folder(self, path):
        files = os.listdir(self.ROOT)
        attrs = []
        for filename in files:
            attr = SFTPAttributes()
            attr.filename = filename
            attr.st_size = os.stat(os.path.join(self.ROOT, filename)).st_size
            attrs.append(attr)
        return attrs

    def open(self, path, flags, attr):
        full_path = os.path.join(self.ROOT, os.path.basename(path))
        return SFTPHandle(full_path)

server = TCPServer(("0.0.0.0", 2222), StreamRequestHandler)
server.serve_forever()
