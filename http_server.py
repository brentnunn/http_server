import mimetypes
import os
import socket
import sys


def response_ok(body, mimetype):
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    resp.append("Content-Type: {}".format(mimetype))
    resp.append("")
    resp.append(body)
    return "\r\n".join(resp)


def response_not_found():
    """returns a 404 Not Found response"""
    resp = []
    resp.append("HTTP/1.1 404 Not Found")
    resp.append("")
    return "\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'
    print >>sys.stderr, 'uri = {}'.format(uri)
    return uri


def resolve_uri(uri):
    """return the content and type of a uri """
    HOME = 'webroot'
    
    if os.path.isdir(HOME + uri):
        return "\r\n".join(os.listdir(HOME + uri)), 'text/plain'
    elif os.path.isfile(HOME + uri):
        f = open(HOME + uri, 'r')
        return f.read(), mimetypes.guess_type(HOME + uri)[0]

    else:
        raise ValueError()


def server():
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    # replace this line with the following once you have
                    # written resolve_uri
                    # response = response_ok()
                    
                    ## uncomment this try/except block once you have fixed
                    ## response_ok and added response_not_found
                    try:
                        content, type = resolve_uri(uri) # change this line
                        response = response_ok(content, type)
                    except ValueError:
                        response = response_not_found()

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
