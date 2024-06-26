#!/usr/bin/env python3
"""
fields: a list of strings representing
all fields to obfuscate
redaction: a string representing by what the
field will be obfuscated
message: a string representing the log line
separator: a string representing by which character
is separating all fields in the log line (message)
"""
import re
import logging
from typing import List
import os
import mysql.connector as mysql

PII_FIELDS = ("email", "phone", "ssn", "password", "name")


def filter_datum(fields, redaction, message, separator):
    """1-main.py should use a regex to replace
    occurrences of certain field values.
    """
    return re.sub(r'({})=[^{}]+'.format(
        '|'.join(fields), separator), r'\1=' + redaction, message
    )


def get_logger() -> logging.Logger:
    """1-main.py"""
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connection.MySQLConnection:
    """1-main.py"""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db = mysql.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return db


def main():
    """1-main.py"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    logger = get_logger()

    for row in rows:
        user_data = "; ".join(f"{field}={value}" for field, value in zip(cursor.column_names, row))
        logger.info(user_data)

    cursor.close()
    db.close()



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        return super().format(record)


if __name__ == "__main__":
    main()