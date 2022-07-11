"""This module deletes and inserts test data into the DB.
"""
from initial_data import master_data

master_data.add_mail_setting()
master_data.add_bcc()
