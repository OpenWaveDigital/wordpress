# user/bin/env python3
# mailchimpUsersRecon_Public.py - réconcilier les listes d'e-mails.

from mailchimp3 import MailChimp
from [–] import apiKey
userName = '[–]'
mcClient = MailChimp(apiKey, userName)

# find list that pertains to subscribers/members
mcClient.lists.all(get_all=True, fields="lists.name,lists.id")
# {'total_items': 2, 'lists': [{'name': 'General', 'id': '101'}, {'name': 'Media', 'id': '102'}]}

memberInfo = mcClient.lists.members.all(list_id='101', get_all=True, fields="members.email_address,members.id")
sourceData = members['members']
emailMaster = []

for entry in sourceData:
    emailMaster.append(entry['email_address'])

# Use emailMaster as variable for list of all e-mails for subscribers.

from pandas.io import sql
from sqlalchemy import create_engine, MetaData, Table, select

import pandas as pd
import pymysql

ServerName = '[–]'
Database = '[–]'
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://' + ServerName + '/' + Database)
conn = engine.connect()
metadata = MetaData(conn)
TableName = '[–]'
conn.begin()

with engine.connect() as conn, conn.begin():
    df = pd.read_sql_table(TableName, conn)

# Use userEmails as variable for list of all e-mails in the Wordpress user table.

userEmails  = df['user_email'].unique().tolist()
lowerUser   = [x.lower() for x in userEmails]
lowerMaster = [x.lower() for x in emailMaster]


migrateEmails = []
for entry in lowerUser:
    if entry not in lowerMaster:
        migrateEmails.append(entry)

print(' ')
print('The following e-mails exist in Wordpress that need to be added to the members list in Mailchimp :')
print(migrateEmails)


# Remember, 'General' Mailchimp list for subscribers is : list_id='101'

for entry in migrateEmails:
    mcClient.lists.members.create('101', {
        'email_address': entry,
        'status': 'subscribed',
    })

print(' ')

if migrateEmails:
    print('These e-mails have been migrated into Mailchimp for you. Thank you.')
else:
    print('There were no e-mails to migrate. Please check back later. Thank you.')

print(' ')