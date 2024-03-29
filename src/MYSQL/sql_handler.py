import os
import mysql.connector
from dotenv import load_dotenv
from src.logger import logging

load_dotenv()

MYSQL_USERNAME=os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
MYSQL_HOST=os.getenv("MYSQL_HOST")
MYSQL_DATABASE_NAME=os.getenv("MYSQL_DATABASE_NAME")


class sql:
    def __init__(self) -> None:
        self.__connection=None
    
    def connection(self):
        if self.__connection==None:
            try:
                logging.info("connecting to MYSQL")
                self.__connection=mysql.connector.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_USERNAME,
                    password=MYSQL_PASSWORD,
                    database=MYSQL_DATABASE_NAME
                )
                logging.info("connected successfully")
                return self.__connection
            except Exception as e:
                logging.info(f"error occured during MYSQL connection {e}")
                raise ConnectionError(f"connection error {e}")
        else:
            return self.__connection
    
    def connection_close(self):
        if self.__connection !=None:
            self.__connection.close()
            self.__connection=None
            logging.info("connection closed successfully")
            
    def start(self,userId:int)->None:
        try:
            conn=self.connection()
            curser=conn.cursor()
            query="INSERT INTO bot_user_settings (userid) VALUES (%s);"
            curser.execute(query,[userId])
            conn.commit()
            self.connection_close()
        except mysql.connector.Error as e:
            logging.info(f"error occured during start {e}")
            
    def update_lang(self,userId:int,lang_code:str)->None:
        try:
            conn=self.connection()
            query="UPDATE bot_user_settings SET lang=%s WHERE userid=%s;"
            curser=conn.cursor()
            curser.execute(query,(lang_code,userId))
            conn.commit()
            self.connection_close()
        except Exception as e:
            logging.info(f"error occured during language update {e}")
            raise ConnectionError()

    def update_mode(self,userId:int,mode:str)->None:
        try:
            conn=self.connection()
            query="UPDATE bot_user_settings SET mode=%s WHERE userid=%s;"
            curser=conn.cursor()
            curser.execute(query,(mode,userId))
            conn.commit()
            self.connection_close()
        except Exception as e:
            logging.info(f"error occured during mode update {e}")
            raise ConnectionError()
    def get_lang(self,userid)->str:
        try:
            conn=self.connection()
            query="SELECT lang FROM bot_user_settings WHERE userid =%s"
            curser=conn.cursor()
            curser.execute(query,[userid])
            rows=curser.fetchall()
            lang=''
            for row in rows:
                lang=row[0]
            self.connection_close()
            return lang
        except Exception as e:
            logging.info(f"error occured during get_lang {e}")
            raise ConnectionError()
    def get_mode(self,userid)->str:
        try:
            conn=self.connection()
            query="SELECT mode FROM bot_user_settings WHERE userid =%s"
            curser=conn.cursor()
            curser.execute(query,[userid])
            rows=curser.fetchall()
            mode=''
            for row in rows:
                mode=row[0]
            self.connection_close()
            return mode
        except Exception as e:
            logging.info(f"error occured during get_mode {e}")
            raise ConnectionError()
    
    def insert_msessage(self,from_,to_,message):
        conn=self.connection()
        query="INSERT INTO bot_messages (from_,to_,message) values(%s,%s,%s);"
        curser=conn.cursor()
        curser.execute(query,[from_,to_,message])
        conn.commit()
        self.connection_close()