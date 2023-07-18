import logging.config
import time
import psutil
import configparser
import pandas as pd
import sqlite3
from os import environ
import sqlalchemy
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

##basic config
##logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#job parameters config
config = configparser.ConfigParser()
config.read('etlConfig.ini')
#[ETL_Log_Job]
LogName = '../frontend/static/Excel/etl_log_job.log'
SrcObject1 = 'all_data.csv'
TgtConnection = 'product_data.db'
TgtObject = 'product_list'

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS product_list (
                                        Order_ID  Integer,
                                        Product string,
                                        Quantity_Ordered integer,
                                        Price_Each float,
                                        Order_Date date ,
                                        Purchase_Address string ,
                                        Month integer,
                                        Sales float
                                    ); """


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        logger.info("Error: {}".format(e))

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logger.info("Error: {}".format(e))
    return c


formatter = logging.Formatter(
    '%(levelname)s:  %(asctime)s:  %(process)s:  %(funcName)s:  %(message)s')
##creating handler
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LogName)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def extraction(SrcObject):

    logger.info('Start Extract Session')
    logger.info('Source Filename: {}'.format(SrcObject))

    try:
        df = pd.read_csv(SrcObject)
        # Creating empty dataframe called 'all_month_data'
        all_months_data = pd.DataFrame()
        # Merging to the previous empty dataframe
        all_months_data = pd.concat([all_months_data, df])
        # Checking the result
        all_months_data.to_csv("all_data.csv", index=False)
        #df_1 = all_months_data.to_csv(SrcObject, index=False)
        logger.info('Records count in source file: {}'.format(len(df.index)))
    except ValueError as e:
        logger.error(e)
        return
    logger.info("Read completed!!")
    return all_months_data


def transformation(SrcObject1):
    try:
        SrcObject1 = pd.read_csv(SrcObject1)
        #Removing Nan Values in our data
        SrcObject1 = SrcObject1.dropna(how='all')
        #Removing rows based on condition, finding 'Or' and delete it
        SrcObject1 = SrcObject1[SrcObject1['Order Date'].str[0:2] != 'Or']
        #Add "Month" Column
        # Get the first 2 characters.
        SrcObject1['Month'] = SrcObject1['Order Date'].str[0:2]
        SrcObject1['Month'] = SrcObject1['Month'].astype(
            'int32')  # turning the data from string to integer
        #Convert 'Quantity Ordered' and 'Price Each' to numeric
        SrcObject1['Quantity Ordered'] = pd.to_numeric(
            SrcObject1['Quantity Ordered'])  # Becoming integer
        SrcObject1['Price Each'] = pd.to_numeric(
            SrcObject1['Price Each'])  # Becoming float
    #Add "Sales" Column
        SrcObject1['Sales'] = SrcObject1['Quantity Ordered'] * \
            SrcObject1['Price Each']
        logger.info('Records count after in source file: {}'.format(
            len(SrcObject1.index)))

        logger.info('Transformation completed, data ready to load!')
    except Exception as e:
        logger.error(e)
        return
    return SrcObject1


def loading(ldf):
    logger.info('Start Load Session')
    try:
        conn = create_connection("product_data.db")
        create_table(conn, sql_create_projects_table)
        logger.info(
            'Connection to {} database established'.format(TgtConnection))
    except Exception as e:
        logger.error(e)
        return
    #3Load dataframe to table
    try:
        for i, row in ldf.iterrows():
            query = """INSERT OR REPLACE INTO {0}(
            Order_ID ,Product ,
            Quantity_Ordered ,
            Price_Each ,Order_Date ,
            Purchase_Address ,Month ,
            Sales ) VALUES('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(
                TgtObject,
                row['Order ID'], row['Product'],
                row['Quantity Ordered'], row['Price Each'],
                row['Order Date'], row['Purchase Address'],
                row['Month'], row['Sales']
                )
            cursor = conn.cursor()
            cursor.execute(query)

    except Exception as e:
        logger.error(e)
        return
    conn.commit()
    logger.info("Data Loaded into target table: {}".format(
        TgtObject))
    return
