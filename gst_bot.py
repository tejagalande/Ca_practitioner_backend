from anticaptchaofficial.imagecaptcha import *
import asyncio
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime
import datetime as dt
import mysql.connector
import os
from datetime import datetime
import logging
import boto3
import time
import base64
import random

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
current_date = datetime.now()
start_date = dt.date( current_date.year if current_date.month >= 4 else current_date.year-1 , 4, 1 )
end_date = dt.date( current_date.year+1 if current_date.month >= 4 else current_date.year , 3, 31 )
mycursor = mydb.cursor()

async def run_bot():
    flg = '222'
    captcha_count = 1
    sql = "select * from notice_download_gst_clients where flag='%s'" % (flg)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    l = len(results)
    cnt = l
    
    if l == 0:
        print('No records are found')
        return
    async with async_playwright() as playwright:
        
        proxy = {
            "server": "https://pr.oxylabs.io",
            "username":"customer-tejas_Ico02-sessid-0040373199-sesstime-10",
            "password":"Overview=RP100"
        }
        
        browser = await playwright.chromium.launch(
            # downloads_path='download',
            headless=False, 
            args=['--start-maximized','--disable-dev-shm-usage','--disable-infobars','--no-sandbox', '--disable-blink-features=AutomationControlled' ],
            # proxy=proxy
            )
        
        # page = await browser.new_page(
            # viewport= {'width': 1920, 'height': 1080},
            # screen= {'width': 1920, 'height': 1080}
        # )
        context = await browser.new_context(
            accept_downloads=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
            )
        # await context.set_default_downloads_path('download')
        page = await context.new_page()
        # await page.evaluate("window.moveTo(0, 0); window.resizeTo(screen.width, screen.height);")
        await page.goto('https://services.gst.gov.in/services/login')  
        # https://eportal.incometax.gov.in/iec/foservices/#/login
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

            await page.wait_for_timeout(1500)
            print('captcha count - ',captcha_count)
            while captcha_count <= 3:
                await page.hover('//*[@id="username"]')
                await page.wait_for_timeout(random.uniform(1000,5000))
                await page.type('//*[@id="username"]', username)
                

                await page.hover('//*[@id="user_pass"]')
                await page.wait_for_timeout(random.uniform(1000,5000))
                await page.type('//*[@id="user_pass"]', password)
                
                
                element = await page.query_selector('#imgCaptcha')
                await element.screenshot(path='captcha.png')
                await page.wait_for_timeout(random.uniform(1000,5000))
                solver = imagecaptcha()
                # solver.set_verbose(1)
                solver.set_key("41b4ba9feb34f95f806ce53143481620")
                solver.set_soft_id(0)
                captcha_text : str = solver.solve_and_return_solution("captcha.png")
                if captcha_text != 0:
                    
                    # captcha_text = captcha_text +"1"
                    print('captcha text - ',captcha_text )
                    await page.type(' //*[@id="captcha"] ', captcha_text)
                    # await page.wait_for_timeout(2000)
                    login_button = page.locator("xpath=/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/form/div[6]/div/button")
                    await login_button.click()
                    await page.wait_for_timeout(random.uniform(1000,5000))
                    
                    # captcha error
                    is_captcha_error = await page.is_visible('body > div.content-wrapper > div.container > div > div.content-pane > div > div > div > div > div > form > div:nth-child(4) > div > span')
                    if is_captcha_error:
                        captcha_content = await page.locator('body > div.content-wrapper > div.container > div > div.content-pane > div > div > div > div > div > form > div:nth-child(4) > div > span').text_content()
                        print(captcha_content)
                        captcha_count+=1
                        await page.locator('//*[@id="username"]').clear()
                        await page.locator('//*[@id="user_pass"]').clear()
 
                    # username or password incorrect message box
                    is_credential_error = await page.is_visible('body > div.content-wrapper > div.container > div > div.content-pane > div > div > div > div > div > div > div > div > alert-message > div')
                    if is_credential_error:
                        crendential_content = await page.locator('body > div.content-wrapper > div.container > div > div.content-pane > div > div > div > div > div > div > div > div > alert-message > div').text_content()
                        print(crendential_content)
                        # captcha_count+=1
                        await page.locator('//*[@id="username"]').clear()
                        await page.locator('//*[@id="user_pass"]').clear()
                        captcha_count = 4
                    
                    if not is_captcha_error or not is_credential_error:
                        break
                else:
                    print("task finished with error "+solver.error_code)
            if captcha_count == 4: 
                captcha_count = 1
                continue
            # Shows prompt window 1
            try:
                prompt1 = page.locator('xpath=//*[@id="adhrtableV"]/div/div/div[2]/a[2]')
                await prompt1.click()
                logging.debug('clicked first prompt')
                await page.wait_for_timeout(2000)
            except Exception as e:
                logging.error(e)
            
            # Shows prompt window 2
            try:
                prompt1 = page.locator('xpath=//*[@id="caNumpopupV"]/div/div/div[2]/a[2]')
                await prompt1.click()
                logging.debug('clicked second prompt')
                await page.wait_for_timeout(2000)
            except Exception as e:
                logging.error(e)
            
            await page.hover('xpath=//*[@id="main"]/ul/li[2]/a')
            await page.wait_for_timeout(random.uniform(1000,5000))
            await page.locator('xpath=//*[@id="main"]/ul/li[2]/a').click()
            
            await page.hover('xpath=//*[@id="main"]/ul/li[2]/ul/li[6]/div/a')
            await page.wait_for_timeout(random.uniform(1000,5000))
            await page.locator('xpath=//*[@id="main"]/ul/li[2]/ul/li[6]/div/a').click()
            
            
            await page.hover('xpath=/html/body/div[2]/div[2]/div/div[2]/div/div/div/ul/li[4]/a')
            await page.wait_for_timeout(random.uniform(1000,5000))
            await page.locator('xpath=/html/body/div[2]/div[2]/div/div[2]/div/div/div/ul/li[4]/a').click()
            
            await page.wait_for_timeout(3000)
            # body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(1)
            # /html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr[1]
            # internal:role=table
            try:
                table = await page.query_selector("internal:role=table")
                await page.wait_for_timeout(4000)
                if table:
                    print('table is exist')
                    rows = await page.query_selector_all("table tbody tr")
                    async with page.expect_download() as download_info:
                        await page.hover("body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8) > div > a")
                        await page.wait_for_timeout(random.uniform(1000,3000))
                        await page.click("body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8) > div > a")
                        await page.wait_for_timeout(2000)
                        pdf_url = page.url
                        await page.wait_for_timeout(4000)
                        # await page.evaluate(f"""
                        #         var xhr = new XMLHttpRequest();
                        #         xhr.open('GET', '{pdf_url}', true);
                        #         xhr.responseType = 'blob';
                        #         xhr.onload = function() {{
                        #             var blob = xhr.response;
                        #             var link = document.createElement('a');
                        #             link.href = URL.createObjectURL(blob);
                        #             link.download = 'file.pdf';
                        #             link.click();
                        #         }};
                        #         xhr.send();
                        #     """)
                        await page.evaluate('document.querySelector("body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8) > div > a").click()')
                        download = await download_info.value
                        await download.save_as(f'download/notice_gst.pdf')
                    # for r in rows:
                        # cells = await r.query_selector_all("td")
                        # data = [ (await cell.text_content()).strip().replace("\n", "").replace("\t", "") for cell in cells]
                        # issuance_date = datetime.strptime(data[4],"%d/%m/%Y").date()
                        
                        # is_within_range = start_date <= issuance_date <= end_date
                        # if is_within_range:
                    #         print(cells[7])
                    #         print(data)
                    #         print('---------')
                    #         # download_link = await r
                    #         # print('inner_html -> ', download_link)
                            # async with page.expect_download() as download_info:
                    #             # await page.click("a .btn btn-download inverseLink")
                    #         # loc  =  page.get_by_role('cell',name= '') 
                    #         # body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8)
                            # body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8) > div > a
                    #         # body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(2) > td:nth-child(8)
                    #         # print(loc)
                                # await cells[7].click()
                                # await page.wait_for_timeout(10000)
                                # download = await page.wait_for_event("download")
                                # download = await download_info.value
                                # await download.save_as('download/notice_order.pdf')
                    # await page.bring_to_front()
                    print('table rows => ',len(rows))
                else:
                    print('table is not exist')
            except Exception as e:
                print(e)
            await page.wait_for_timeout(10000)
            # issuance_date = await page.locator('body > div.content-wrapper > div.container > div > div.content-pane > div > div.tabpane > form > div:nth-child(7) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(5)').text_content()
            # print('Date of Issuance - ', datetime.strptime(issuance_date, "%d/%m/%Y").date() )
            
            await page.wait_for_timeout(2000)
            # await browser.close()

asyncio.run(run_bot())




            # async with page.expect_download() as download_info:
            #     await page.click('#alternatives > div.text-center > div > a')
            # download = await download_info.value
            # await download.save_as('sample.pdf')
            # time.sleep(5)
            # async with page.expect_download() as download_info:
            #     await page.click('#alternatives > div.text-center > div > a')
            # download = await download_info.value
            # await download.save_as('download/sample-new.pdf')