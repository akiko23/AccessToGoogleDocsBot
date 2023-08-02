from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from jinja2 import Template

from config import db

with open("admin.html", "r") as f:
    text_for_tm = f.read()
tm = Template(text_for_tm)

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        users = db.get_all_users()
        self.wfile.write(tm.render(users=users).encode())



if __name__ == "__main__":
    run(handler_class=HttpGetHandler)


