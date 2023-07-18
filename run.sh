#!/bin/bash


pip install -r requirements.txt

cd backend 

gunicorn app:app
