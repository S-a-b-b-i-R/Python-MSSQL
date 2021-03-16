import pyodbc
import pandas as pd
import sqlalchemy
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


conn1 = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                       'SERVER=DESKTOP-7797FGT;'
                       'DATABASE=master;'
                       'trusted_connection=yes;'
                       )
print('Step 1 is successful, connection with the server is established')
conn1.autocommit = True
cursor1 = conn1.cursor()

SQL_command = '''
                CREATE DATABASE Trial
                
                
                ON     
                (
                     NAME = 'Phase'
                ,    FILENAME='C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\Trial.mdf' 
                ,    SIZE = 4096KB 
                ,    FILEGROWTH = 4096KB 
                ) 
                LOG ON  
                (
                    NAME = 'Phase_log'
                ,   FILENAME='C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\LOG\Trial_log.ldf' 
                ,   SIZE = 4096KB 
                ,   FILEGROWTH = 10%
                )'''

# Make the commit
complete = cursor1.execute(SQL_command)
complete.commit()

print('Step 2 is successful, new database is created')


# Make two new connections using sqlalchemy
db1 = sqlalchemy.create_engine('mssql+pyodbc://DESKTOP-7797FGT/COMPANY?trusted_connection=yes&driver=ODBC+Driver+17'
                               '+for+SQL+Server')
db2 = sqlalchemy.create_engine('mssql+pyodbc://DESKTOP-7797FGT/Trial?trusted_connection=yes&driver=ODBC+Driver+17+for'
                               '+SQL+Server')


@scheduler.scheduled_job('interval', seconds=30)
def timed_job():
    # Copy the table "EMPLOYEE" from COMPANY to Trial

    query = '''SELECT * FROM [dbo].[EMPLOYEE]'''
    df = pd.read_sql(query, db1)
    df.to_sql('test_table', db2, schema='dbo', index=False, if_exists='replace')

    print('(*) [test_table] copied.')


scheduler.start()