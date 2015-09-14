#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import logging

SEARCH_QUERY_LIKE = "SELECT * FROM ICD WHERE DESCRIPTION LIKE ?"
SEARCH_QUERY_LIKE_ICD = "SELECT * FROM ICD WHERE ICD LIKE ?"

class ICDdb:
    def __init__(self, path):
        self.db_path = path
        self.lgr = logging.getLogger('ICDdb')
        self.__connected = False
        self.con = None
        self.c = None
        self.sql = ""

        if not os.path.isfile(path):
            self.lgr.debug(' invalid path %s', self.db_path)

    @property
    def connected(self):
        return self.__connected

    @connected.setter
    def connected(self, value):
        self.__connected = value

    def test_db(self):
        pass

    def connect(self):
        try:
            self.con = sqlite3.connect(self.db_path, check_same_thread=False)
            self.c = self.con.cursor()
        except:
            self.lgr.debug('connection error %s', self.db_path)

        if self.con is not None:
            self.connected = True

    def __exec_data_query(self, sql, data):
        self.sql = sql
        self.c.execute(self.sql, data)

        try:
            self.c.execute(self.sql, data)
        except sqlite3.Error as msg:
            self.lgr.error('Error on exec_str_data \n\n %s %s\n\tSQL: %s \n\tdata %s',
                           msg, self.sql, data)
        return self.c.fetchall()

    def get_like_icd(self, seach_txt):
        search_data = ("%" + seach_txt + "%",)
        answer = None
        if self.connected:
            answer = self.__exec_data_query(SEARCH_QUERY_LIKE_ICD, search_data)
        else:
            self.lgr.debug('Not connected!')

        if answer is not None:
            return answer

        self.lgr.debug('not found %s', seach_txt)
        return False

    def get_like_description(self, seach_txt):
        search_data = ("%" + seach_txt + "%",)
        answer = None
        if self.connected:
            answer = self.__exec_data_query(SEARCH_QUERY_LIKE, search_data)
        else:
            self.lgr.debug('Not connected!')

        if answer is not None:
            return answer

        self.lgr.debug('not found %s', seach_txt)
        return False
