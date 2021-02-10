from __future__ import absolute_import, unicode_literals

from .models import *
from django.conf import settings
import requests
from datetime import datetime
import csv, zipfile
from io import TextIOWrapper, StringIO
import os
from django.core.paginator import Paginator

from celery import shared_task
import time


# ALL esentian params for easy config
DIR = settings.BASE_DIR + '/datasets'
target_zip = f"{DIR}/zip/target.zip"
target_csv = f'{DIR}/targer.csv'

date = datetime.now()
today = f"{date.strftime('%d%m%y')}"

url = f"https://www.bseindia.com/download/BhavCopy/Equity/EQ{today}_CSV.ZIP"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
response = requests.get(url, headers=headers, timeout=5)

columns = 'CODE,NAME,SC_GROUP,SC_TYPE,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,NO_TRADES,VOLUME,NET_TURNOV,TDCLOINDI'


# Unzip downloaded zip file from Bhavcopy
def unzip():
    with zipfile.ZipFile(target_zip, "r") as zip_ref:
        for file in zip_ref.namelist():
            data = []
            with zip_ref.open(file) as myfile:
                reader = csv.reader(TextIOWrapper(myfile, 'utf-8'))
                for row in reader:
                    data.append(row)
            return data


# Write on CSV file 
# edit with relevent header
def writeCSV(data):
    linecount = 0
    f = StringIO(columns)
    reader = csv.reader(f, delimiter=',')

    for row in reader:
        header_row = row

    with open(target_csv, "w") as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n'
        )

        for row in data:
            if linecount == 0:
                csv_writer.writerow(header_row)
                linecount += 1
            else:
                csv_writer.writerow(row)
                linecount += 1

        csv_file.close()


def fetch():
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    with open(target_zip, "wb") as file:
        file.write(response.content)
        file.close()

        data = unzip()
        writeCSV(data)


# Automated Task from celery-beat 
# Configurable from Admin panel
# Download data from Bhavcopy
# Update new records to DB
@shared_task
def set_data():
    fetch()
    BSE.objects.all().delete()

    with open(target_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            _, bse = BSE.objects.get_or_create(CODE=row["CODE"],
                                               NAME=row["NAME"],
                                               OPEN=row["OPEN"],
                                               HIGH=row["HIGH"],
                                               LOW=row["LOW"],
                                               CLOSE=row["CLOSE"])

            # bse.save()


# deliver data from model to view
def get_data(pagination, page_number=None, key=None):
    if key:
        data = BSE.objects.filter(NAME__contains=key)

    else:
        data = BSE.objects.all()

    if pagination:
        # 25 row per page
        paginator = Paginator(data, 25)
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = data

    return page_obj


def get_details(code):
    data = BSE.objects.get(CODE=code)

    return data


# Create CSV file
def create_cv(code):
    data = get_details(code)
    dir_name = os.path.join(DIR, "details.csv")

    with open(dir_name, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow([data.CODE, data.NAME.strip(), data.OPEN, data.HIGH, data.LOW, data.CLOSE])

        file.close()

    return dir_name, data.NAME.strip()
