#!/usr/bin/env python

import socket;

if "__main__" == __name__:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.connect(('192.168.0.140', 10003));
    sock.send('HB\r\n');

    szBuf = sock.recv(1024);
    print("recv " + szBuf);
    sock.close();
    print("end of connect");
