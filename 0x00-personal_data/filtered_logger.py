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


def filter_datum(fields, redaction, message, separator):
    """1-main.py should use a regex to replace
    occurrences of certain field values.
        """
    return re.sub(r'({})=[^{}]+'.format(
        '|'.join(fields), separator), r'\1=' + redaction, message
    )


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
