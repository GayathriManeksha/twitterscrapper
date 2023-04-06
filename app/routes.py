from flask import Flask, request, flash, url_for, redirect, render_template 
from app import app
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import json

def unametoid(username):
    url = 'https://twitter.com/{}'.format(username)
    print(url)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    user_id = soup.find('script', {'data-testid': 'UserProfileSchema-test'})
    print(user_id)
    data = json.loads(user_id.string)
    print(data['author']['identifier'])
    return data['author']['identifier']

def idtouname(numid):
    url2='https://twitter.com/i/user/{}'.format(numid)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    user_id = soup.find('script', {'data-testid': 'UserProfileSchema-test'})
    # print(user_id.string)
    data = json.loads(user_id.string)
    print(data['author']['additionalName'])
    return data['author']['additionalName']

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        bt=request.form.get('bt')
        if bt=='btn1':
            print(request.form['username'])
            value=unametoid(request.form['username'])
            return render_template('base.html',valueid=value)
        else:
            print(request.form['numid'])
            value=idtouname(request.form['numid'])
            return render_template('base.html',valueun=value)
    return render_template('base.html')