import asyncio
from playwright.async_api import async_playwright, TimeoutError

import mysql.connector
import os
from datetime import datetime
import logging
import boto3
import time
import base64


# logcat_path = f"gst_logs_{int(time.time())}.log"

# logging.basicConfig(
#     # encoding='utf-8',
#     format=
#     '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%Y-%m-%d:%H:%M:%S',
#     level=logging.DEBUG,
#     filename=logcat_path,
# )


mydb = mysql.connector.connect(
    host="193.203.160.234",
    user="admin",
    password="Useradmin(100)",
    database="notice_management",
    # port="3306"
)

mycursor = mydb.cursor()


async def run_bot():
    flg = 222
    sql = "select * from notice_download_it_clients where flag='%s'" % (flg)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    l = len(results)
    cnt = l
    
    if l == 0:
        print('No records are found')
        return
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
        headless=False, 
        args=['--start-maximized','--disable-dev-shm-usage','--disable-infobars','--no-sandbox', '--disable-blink-features=AutomationControlled' ]
        )
        
        page = await browser.new_page(
            # viewport= {'width': 1920, 'height': 1080},
            # screen= {'width': 1920, 'height': 1080}
        )
        
        await page.goto('https://eportal.incometax.gov.in/iec/foservices/#/login') 
        
        await page.wait_for_timeout(5000)
        for row in results:
            name = row[1]
            username = base64.b64decode(row[2]).decode()
            password = base64.b64decode(row[3]).decode()
            id = row[0]
            name = 'G' + str(row[0])
            logging.debug('id= %s', id)
            logging.debug('name= %s',name)
            logging.debug('username= %s', username)
            print('id - ', id)
            print('username - ',username)
            print('password - ',password)
            logging.debug('password= %s',password)
            
            await page.type('//*[@id="panAdhaarUserId"]', username)
            
            await page.wait_for_timeout(1000)
            
            await page.locator('xpath=//*[@id="maincontentid"]/app-login/div/app-login-page/div/div[2]/div[1]/div[2]/button').click()
            
            await page.wait_for_timeout(1000)
            
            await page.locator('xpath=//*[@id="passwordCheckBox"]/label/div').click()
            
            await page.type('//*[@id="loginPasswordField"]', password)
            
            await page.wait_for_timeout(1000)
            
            await page.locator('xpath=//*[@id="maincontentid"]/app-login/div/app-password-page/div[1]/div[2]/div[1]/div[5]/button').click()
            await page.wait_for_timeout(5000)
            request_error = await page.is_visible('#mat-error-0 > div')
            print('is visible -', request_error)
            # #mat-error-0 > div
            if request_error:
                print('request error is shown')
                await page.locator('xpath=//*[@id="maincontentid"]/app-login/div/app-password-page/div[1]/div[2]/div[1]/div[5]/button').click()
                await page.wait_for_timeout(3000)
            
            duplicate_login = await page.is_disabled('#loginMaxAttemptsPopup > div > div > div.modal-footer > button.defaultButton.primaryButton.primaryBtnMargin', timeout=5000, strict=False)
            print('LOGIN HERE text is displayed? ', duplicate_login)
            
            await page.wait_for_timeout(20000)
        await browser.close()
        

asyncio.run(run_bot())