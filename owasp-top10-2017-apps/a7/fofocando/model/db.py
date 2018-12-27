#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

class DataBase:
    def __init__ (self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db = MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.database,charset='utf8')
        self.c = self.db.cursor()

    def connect(self):
        self.db = MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.database)
        self.c = self.db.cursor()

    def get_user_password(self, username):
        try:
			self.c.execute("SELECT password FROM users WHERE user = %s", [username])
			user_password = self.c.fetchone()

        except (AttributeError, MySQLdb.OperationalError):
			self.connect()
			self.c.execute("SELECT password FROM users WHERE username = %s", [username])
			user_password = self.c.fetchone()

        except MySQLdb.Error, e:
            try:
				message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return message , 0
            except IndexError:
				message = "MySQL Error: %s" % str(e)
				return message , 0

        return user_password, 1

    def insert_user(self, user, password):
        try:
            self.c.execute("INSERT INTO users (user, password) VALUES (%s, %s);",(user, password))
            self.db.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.c.execute("INSERT INTO users (user, pasword) VALUES (%s, %s);",(user, password))
            self.db.commit()
        except MySQLdb.Error, e:
        	try:
        		message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        		return message , 0
        	except IndexError:
        		message = "MySQL Error: %s" % str(e)
        		return message , 0
        return "" , 1


    def get_latest_gossips(self, limit, offset):
        try:
            self.c.execute("SELECT id, text, author, title, subtitle, date FROM gossips LIMIT %s,%s", [limit, offset])
            gossips = self.c.fetchall()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.c.execute("SELECT id, text, author, title, subtitle, date FROM gossips LIMIT %s,%s", [limit, offset])
            gossips = self.c.fetchall()
        except MySQLdb.Error, e:
            try:
                message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return message , 0
            except IndexError:
                message = "MySQL Error: %s" % str(e)
                return message , 0

        return gossips , 1

    def search_gossips(self, limit, offset, search_str):
        try:
            self.c.execute("SELECT id, text, author, title, subtitle, date FROM gossips WHERE title  LIKE %s LIMIT %s,%s", ["%"+ search_str + "%", limit, offset])
            gossips = self.c.fetchall()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.c.execute("SELECT id, text, author, title, subtitle, date FROM gossips WHERE title  LIKE %s LIMIT %s,%s", ["%"+ search_str + "%", limit, offset])
            gossips = self.c.fetchall()
        except MySQLdb.Error, e:
            try:
                message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return message , 0
            except IndexError:
                message = "MySQL Error: %s" % str(e)
                return message , 0

        return gossips , 1

    def get_gossip(self, id):
        try:
            self.c.execute("SELECT id, text, author, title, subtitle, date FROM gossips WHERE id = %s", [id])
            gossip = self.c.fetchone()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.c.execute("SELECT id, text, author, title, subtitle, date FROM gossips WHERE id = %s", [id])
            gossips = self.c.fetchone()
        except MySQLdb.Error, e:
            try:
                message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return message , 0
            except IndexError:
                message = "MySQL Error: %s" % str(e)
                return message , 0
        return gossip , 1

    def get_comments(self, id):
        try:
            self.c.execute("SELECT author, comment, date FROM comments WHERE gossip_id = %s", [id])
            comments = self.c.fetchall()
            # comments = (1,2)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.c.execute("SELECT author, comment, date FROM comments WHERE gossip_id = %s", [id])
            comments = self.c.fetchall()
        except MySQLdb.Error, e:
            try:
                message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return message , 0
            except IndexError:
                message = "MySQL Error: %s" % str(e)
                return message , 0
        if comments == ():
            return None, 1
        return comments , 1

    def post_comment(self, author, comment, gossip_id, date):
        try:
            self.c.execute("INSERT INTO comments (author, comment, gossip_id, date) VALUES (%s, %s, %s, %s);",(author, comment, gossip_id, date))
            self.db.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.c.execute("INSERT INTO comments (author, comment, gossip_id, date) VALUES (%s, %s, %s, %s);",(author, comment, gossip_id, date))
            self.db.commit()
        except MySQLdb.Error, e:
            try:
            	message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            	return message , 0
            except IndexError:
            	message = "MySQL Error: %s" % str(e)
            	return message , 0
        return "" , 1

    def post_gossip(self, author, text, title, subtitle, date):
        try:
            self.c.execute("INSERT INTO gossips (author, text, title, subtitle, date) VALUES (%s, %s, %s, %s, %s);",(author, text, title, subtitle, date))
            self.db.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.c.execute("INSERT INTO gossips (author, text, title, subtitle, date) VALUES (%s, %s, %s, %s, %s);",(author, text, title, subtitle, date))
            self.db.commit()
        except MySQLdb.Error, e:
        	try:
        		message = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        		return message , 0
        	except IndexError:
        		message = "MySQL Error: %s" % str(e)
        		return message , 0
        return "" , 1
