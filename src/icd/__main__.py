#!/usr/bin/python3
# -*- coding: utf-8 -*-

from application import Application
import sys

def main():
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

if __name__ == '__main__':    
    main()
