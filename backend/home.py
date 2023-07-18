from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user
import sqlite3
from sqlalchemy.types import Integer, Text, String, DateTime
from flask import current_app
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, send_file
import os
from os import environ
import logging.config
import time
import psutil
from logs import *
import configparser
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import configparser
import pandas as pd

home = Blueprint('home', __name__, static_url_path='/static',
                 static_folder='../frontend/static',
                 template_folder='../frontend/template')
login_manager = LoginManager()
login_manager.init_app(home)

con = sqlite3.connect("RecodsImport.db")
con.execute(
    "create table if not exists data(pid integer primary key,exceldata TEXT)")
con.close()
##basic config
##logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LogName)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@home.route('/home', methods=['GET', 'POST'])
@login_required
def index():
    con = sqlite3.connect("RecodsImport.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data")
    data = cur.fetchall()
    con.close()

    if request.method == 'POST':
        uploadExcel = request.files['uploadExcel']
        if uploadExcel.filename != '':
            filepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'], uploadExcel.filename)
            uploadExcel.save(filepath)
            ###########################
            print("#### ETL process #####")
            logger.info('##### ETL Process Initialized #####')
            ###########################
            ##extract
            start = time.time()
            start1 = time.time()
            job_log = extraction(filepath)
            end1 = time.time() - start1
            logger.info('Extract CPU usage {}%'.format(psutil.cpu_percent()))
            logger.info("Extract function took : {} seconds".format(end1))
            ##transformation
            start2 = time.time()
            ldf = transformation(SrcObject1)
            end2 = time.time() - start2
            logger.info('Transform CPU usage {}%'.format(psutil.cpu_percent()))
            logger.info("Transformation took : {} seconds".format(end2))

            ##load
            start3 = time.time()
            loading(ldf)
            end3 = time.time() - start3
            logger.info('Load CPU usage {}%'.format(psutil.cpu_percent()))
            logger.info("Load took : {} seconds".format(end3))
            end = time.time() - start
            logger.info("ETL Job took : {} seconds".format(end))
            ##p = psutil.Process()
            ##ls = p.as_dict()
            ##print(p.as_dict())
            logger.info('Session Summary')
            logger.info('RAM memory {}% used:'.format(
                psutil.virtual_memory().percent))
            logger.info('CPU usage {}%'.format(psutil.cpu_percent()))
            print("multiple threads took : {} seconds".format(end))
            #########################
            logger.info('#####  ETL Process finished ##### ')
            #########################
            con = sqlite3.connect("RecodsImport.db")
            cur = con.cursor()
            cur.execute("insert into data(exceldata)values(?)",
                        (uploadExcel.filename,))
            con.commit()
            flash("Excel Sheet Upload Successfully", "success")
            con = sqlite3.connect("RecodsImport.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from data")
            data = cur.fetchall()
            con.close()
            return render_template("home.html", data=data)

    return render_template("home.html", data=data)


@home.route('/view_excel/<string:id>')
def view_excel(id):
    con = sqlite3.connect("product_data.db")
    # con.row_factory = sqlite3.Row
    # cur = con.cursor()
    # cur.execute("select * from product_list LIMIT 14")
    dataETL = pd.read_sql(
        "SELECT * FROM product_list LIMIT 14", con=con, index_col=None)
    after_data = dataETL.head(4)
    con.close()

    con_etl = sqlite3.connect("RecodsImport.db")
    con_etl.row_factory = sqlite3.Row
    cur_etl = con_etl.cursor()
    cur_etl.execute("select * from data where pid=?", (id))
    data = cur_etl.fetchall()

    for itr in data:
        path_be = os.path.join("../frontend/static/Excel/", itr[1])
        print(itr[1])
        data = pd.read_csv(path_be)
        before_data = data.head(4)
    con_etl.close()

    return render_template("view_excel.html",
                           data=before_data.to_html(index=False, classes="table table-bordered").replace(
                               '<th>', '<th style="text-align:center">'),
                           dataETL=after_data.to_html(
                               index=False, classes="table table-bordered").replace('<th>', '<th style="text-align:center">')
                           )


@home.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sqlite3.connect("RecodsImport.db")
        cur = con.cursor()
        cur.execute("delete from data where pid=?", [id])
        con.commit()
        flash("Record Deleted Successfully", "success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("home.index"))
        con.close()
        return redirect(url_for("home.index"))
        con.close()
        return redirect(url_for("home.index"))
        con.close()
        con.close()


@home.route('/downlaod', methods=['GET'])
def download():
    full_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], "etl_log_job.log")
    print(full_path)
    if full_path:
        return send_file(full_path)
    else:
        render_template("home.html")
