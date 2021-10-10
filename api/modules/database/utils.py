import hashlib
from typing import List


def encrypt_string(input: str):
    """
    Utility function for applying general encryption (sha256 algorithm) to any string

    :param input: String to which apply the encryption
    :return: String with the hex representation of the encrypted input string
    """
    h = hashlib.new('sha512_256')
    h.update(str.encode(input))
    return str(h.hexdigest())


def generate_sql_update_set_formatted_string(keys_list: List[str]):
    """
    Utility function for generating a formatted string for building dynamic
    SQL UPDATE query strings. Takes each string in the input list and
    returns a string that can be inserted as part of the 'SET' segment of an
    SQL UPDATE query

    :param keys_list: List of strings where every string is the name of a column of a given table
    :return: A string of the format 'column = :column, column = :column, ...'
    """

    return ", ".join([f"{key} = :{key}" for key in keys_list])
