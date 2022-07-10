"""This module deletes and inserts master data into the DB.
"""
from contact.models import Bcc, MailSetting

def add_mail_setting():
    """This inserts records of mail setting.
    """
    # DB データを全削除
    for record in MailSetting.objects.all():
        record.delete()

    # DBにデータを追加
    setting = MailSetting()
    setting.sender = 'example@hogehoge.com'
    setting.save()

def add_bcc():
    """This inserts records of BCC.
    """
    # DB データを全削除
    for record in Bcc.objects.all():
        record.delete()

    # DBにデータを追加
    bcc1 = Bcc(email = 'example@hoghoge.com')
    bcc1.save()
    bcc2 = Bcc(email = 'example2@hoghoge.com')
    bcc2.save()
