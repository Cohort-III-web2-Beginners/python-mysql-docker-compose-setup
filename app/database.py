import os
import pymysql
from contextlib import contextmanager
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.user = os.getenv("DB_USER")
        self.database = os.getenv("DB_DATABASE")
        self.password = os.getenv("DB_PASSWORD")
        self.connection = os.getenv("DB_CONNECTION")


    def wait_for_db(self, max_retries=30, retry_interval=5):
        logger.info(f"waiting for database connection {self.host}:{self.port}")
        for attempt in range(max_retries):
            try:
                connection = pymysql.connect(
                    host = self.host,
                    user = self.user,
                    password = self.password,
                    port=self.port
                )

                connection.close()

                logger.info("Database Connection Successful!")

                return True
            except pymysql.Error as e:
                logger.warning(f"Database connection failed: {e}")
                # do more error handling
                if attempt < max_retries - 1:
                    time.sleep(retry_interval)
                raise

    def get_connection(self):
            try:
                connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,
                    connect_timeout=10
                )
                logger.info("Successfully connected to MySQL database")
                return connection
            except pymysql.Error as e:
                logger.error(f"Error connecting to MySQL database: {e}")
                raise
        
    @contextmanager
    def get_cursor(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            yield cursor
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.error(f"Error getting cursor: {e}")
            raise
        finally:
            cursor.close()
            connection.close()

db = DatabaseConnection()