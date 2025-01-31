from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from anticaptchaofficial.imagecaptcha import *
from webdriver_manager.chrome import ChromeDriverManager
# from PIL import Image
from selenium.webdriver.chrome.options import Options
import json
from tkinter import messagebox
from lib2to3.pgen2 import driver
from xml.etree.ElementPath import xpath_tokenizer
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
import os
from datetime import datetime
import logging
import boto3
import base64
import undetected_chromedriver as uc

option = Options()
# chrome_options.add_experimental_option("detach", True)
logcat_path = f"gst_logs_{int(time.time())}.log"
# os.path.dirname("D:\\python_codes\\gst_logs_"+ str(datetime.now()) +".log")
logging.basicConfig(
    # encoding='utf-8',
    format=
    '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG,
    filename=logcat_path,
)

os.system("title gst")
wait = WebDriverWait(driver, 40)
action = ActionChains(driver)

mydb = mysql.connector.connect(
    host="193.203.160.234",
    user="admin",
    password="Useradmin(100)",
    database="notice_management",
    # port="3306"
)

#obtain browser tab window
# c = driver.window_handles[1]

# mydb = mysql.connector.connect(
#     host="127.0.0.1",
#     user="admin",
#     password="Adminuser%5",
#     database="notice_management"
# )

mycursor = mydb.cursor()



def dot_intimation(id :int, refid : str, driver, dir_path :str):
    

    
    try:
        is_no_intimation = driver.find_element( By.XPATH,
        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/table/tbody/tr'
        ).is_displayed()
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/table/tbody/tr/td
        # logging.debug(f'length of the table={intimation_table_length}' )
    except Exception as e: logging.error(e)
    
    new_data = False
    if not is_no_intimation:
        logging.info( '------------------------------------------------------------------' )
        logging.info('Intimation Table')
        logging.info('------------------------------------------------------------------')
        logging.debug(f'client id - {id}')
        table_len = driver.find_elements(
            By.XPATH, 
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span')
        logging.debug(f'dot intimation table length - {len(table_len)}')
    
   
        if len(table_len) > 0:
            i_noticetype = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[1]/span'
            ).text
            i_ref = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[2]/span'
            ).text
            i_issue_date = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[3]/span'
            ).text
            i_due_date = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[4]/span'
            ).text
            i_section = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[5]/span'
            ).text

            i_cnf_issue_date = datetime.strptime( i_issue_date, "%d/%m/%Y" ).strftime( '%Y-%m-%d')
            i_cnf_due_date = datetime.strptime( i_due_date, "%d/%m/%Y" ).strftime( '%Y-%m-%d')

            logging.debug(f'intimation ={i_noticetype}')
            logging.debug( f'intimation refrence={i_ref}')
            logging.debug(f'intimation issue date={i_issue_date}')
            logging.debug(f'intimation Due Date={i_due_date}')
            logging.debug( f'intimation Section={i_section}')
            logging.debug( f'converted issue date={i_cnf_issue_date}')
            logging.debug( f'converted due date={i_cnf_due_date}')

            status = "Not Started"
            try:
                sql = "select reference_num,attachment from notice_download_gst_intimation_dot where client_id='%s' and reference_id='%s' and reference_num='%s' " % (
                    id, refid, i_ref)
                mycursor.execute( sql)
                # Fetch all the rows in a list of lists.
                intimation_result1 = mycursor.fetchall()
                logging.debug(  intimation_result1 )
            except Exception as e:
                logging.debug(e)
            
            file_list = []
            
            for i in range( 1, len(table_len)+1 ):
                i_notice_name = driver.find_element(
                    By. XPATH,
                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span[%s]/p/a'% (i)
                ).text        
                #  here
                # if result is empty
                if len(intimation_result1) == 0  :

                    # download notice
                    download = driver.find_element(
                        By.XPATH,
                        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span[%s]/p/a'
                        % (i)
                    )
                    
                    download.click()
                    file_list.append(i_notice_name)
                    new_data = True
                    logging.info(f'{i_notice_name} is downloaded')
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
                    
                # if result has some data
                if len(intimation_result1) < len(table_len) and len(intimation_result1) > 0 :
                    logging.debug('some data are available')
                    def exist():
                        logging.debug('start exist function')
                        for i in intimation_result1:
                            logging.debug('checking current notice file')
                            if i[1] ==  i_notice_name:
                                return True
                        return False
                    
                    # download notice
                    logging.debug(f'exist function returned {exist()}')
                    if not exist():
                        logging.debug('exist if block start')
                        download = driver.find_element(
                            By.XPATH,
                            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span[%s]/p/a'
                            % (i) )
                        download.click()
                        file_list.append(i_notice_name)
                        new_data = True
                        # logging.info('line no 928')
                        logging.info(f'{i_notice_name} intimation is downloaded')
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)
                    else:
                        logging.debug('dot intimation is already present.' )
            if len(intimation_result1) != len(table_len): monitor_download_progress(dir_path, len(table_len) if len(intimation_result1) == 0 else len(table_len) - len(intimation_result1) )
            if len(file_list) > 0:
                for i in file_list:
                    try:
                        logging.debug('In try block' )
                        mycursor.execute(
                            "INSERT INTO notice_download_gst_intimation_dot( client_id,notice_type, attachment, reference_num,issue_date,due_date,section,status,reference_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (id, i_noticetype ,i , i_ref,i_cnf_issue_date, i_cnf_due_date, i_section,status, refid ))
                        mydb.commit()
                    
                    except Exception as e:
                        logging.error(e)
            # client_id category type reference_or_order_num issue_date due_date order_date section personal_hearing status attachment
            mycursor.execute("INSERT INTO determination_of_tax (client_id, category, type, reference_or_order_num, issue_date, due_date, section,  status, attachment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (id, "Intimation", i_noticetype, i_ref, i_cnf_issue_date, i_cnf_due_date, i_section, status, json.dumps(file_list))
                             ) 
            
            mydb.commit()
            logging.debug(f'last row added id in dot table - ${mycursor._last_insert_id}')
    # driver.quite()
    return new_data

def dot_notice(id :int, refid : str, driver, dir_path : str):
    logging.debug(f'user id:{id}')
    try:
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody
        time.sleep(1)
        notice_table = driver.find_elements(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr'
        )
        
        logging.debug( f'Notice Table Length ###### = {len(notice_table)}')
        
        n_noticetype = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[1]/span'
        ).text
        n_ref = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[2]/span'
        ).text
        n_issue_date = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[3]/span'
        ).text
        n_due_date = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[4]/span'
        ).text
        
        person_hearing = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[5]'
        ).text
        logging.debug(f'n Personal Hearing : {person_hearing}' )
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[5]/span[1]
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[5]
        
        n_section = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span'
        ).text

        n_cnf_issue_date = datetime.strptime(  n_issue_date,  "%d/%m/%Y").strftime('%Y-%m-%d')
        n_cnf_due_date = datetime.strptime( n_due_date,    "%d/%m/%Y" ).strftime('%Y-%m-%d')
        status = "Not Started"

        logging.debug(f'n notice type : {n_noticetype}')
        logging.debug(f'n  n refrence: {n_ref}')
        logging.debug( f'n issue date : {n_issue_date}')
        logging.debug( f'n Due Date : {n_due_date}')
        logging.debug(f'n Section : {n_section}')
        logging.debug(f'n Personal Hearing : {person_hearing}' )
        logging.debug( f'n converted issue date : {n_cnf_issue_date}')
        logging.debug( f'converted due date : {n_cnf_due_date}')
        
        table_body = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody'
        )
        entries = table_body.find_elements(By.TAG_NAME, 'tr')

        notice_counts = table_body.find_elements( By.TAG_NAME, 'a')

        logging.debug( f'count of links in table : {len(notice_counts)}')
        
        try:
            sql = "select reference_id, attachment from notice_download_gst_notice_dot where client_id='%s' and reference_id='%s' and ref_id='%s' " % (
                id, n_ref, refid)
            mycursor.execute( sql)
            # Fetch all the rows in a list of lists.
            gst_other_notice_result = mycursor.fetchall()

            logging.debug(f'gst notices table count : {len(gst_other_notice_result)}')
            logging.debug(f'gst notices table : {gst_other_notice_result}')
        except Exception as e:
            logging.debug(e)
        
        file_list = []
        new_data = False
        for i in range( 1, len(notice_counts) + 1):
            # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[1]/p/a
            n_notice_name = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[%s]/p/a'
                % (i)).text

            # if result is empty
            if len(gst_other_notice_result) == 0  :
                # download notice
                download = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[%s]/p/a'
                    % (i)
                )
                
                download.click()
                file_list.append(n_notice_name)
                new_data = True
                logging.info(f'DOT {n_notice_name} notice is downloaded')
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

            # if result has some data
            if len(gst_other_notice_result) < len(notice_counts) and len(gst_other_notice_result) > 0 :
                logging.debug('some data are available')
                def notice_exist1():
                    logging.debug('start exist function')
                    for i in gst_other_notice_result:
                        logging.debug('checking current notice file')
                        if i[1] ==  n_notice_name:
                            return True
                    return False
                    
                # download notice
                logging.debug(f'exist function returned {notice_exist1()}')
                if not notice_exist1():
                    logging.debug('exist if block start')
                    # /html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[1]/p/a
                    download = driver.find_element(
                        By.XPATH,
                        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[%s]/p/a'
                        % (i)
                    )
                
                    download.click()
                    file_list.append(n_notice_name)
                    new_data = True
                    # logging.info('line no 928')
                    logging.info(f'DOT {n_notice_name} is downloaded')
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
                else:
                    logging.debug('notice is already present.' )
        time.sleep(1)
        if len(gst_other_notice_result) != len(notice_counts): monitor_download_progress(dir_path, len(notice_counts) if len(gst_other_notice_result) == 0 else len(notice_counts) - len(gst_other_notice_result) )
        if len(file_list) > 0:
            for i in file_list:
                try:
                    mycursor.execute(
                        "INSERT INTO notice_download_gst_notice_dot ( client_id, notice_type, attachment, reference_id, issue_date, due_date, section_num, personal_hearing, status, ref_id ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (id, n_noticetype ,i , n_ref, n_cnf_issue_date, n_cnf_due_date, n_section,  person_hearing, status, refid ))
                    mydb.commit()
                    logging.debug('In try block' )
                except Exception as e:
                    logging.error(e)
        # driver.back()
        mycursor.execute("INSERT INTO determination_of_tax (client_id, category, type, reference_or_order_num, issue_date, due_date, section, personal_hearing, status, attachment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (id, "Notice", n_noticetype, n_ref, n_cnf_issue_date, n_cnf_due_date, n_section, person_hearing ,status, json.dumps(file_list))
                             ) 
            
        mydb.commit()
        logging.debug(f'last row added id in dot table - ${mycursor._last_insert_id}')
    except Exception as e:
        logging.error(e)
    logging.debug('notice tab section end here')
    time.sleep(2)
    return new_data
    
def dot_order(id :int,refid : str, driver, dir_path: str):
    logging.debug(f'user id:{id}')
    try:
        # In the order tab
        status = "Not Started"
        time.sleep(2)
        logging.debug('order tab selected')
        logging.debug('In try block')
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[3]
        
        # driver.quit()

        # typeoforder=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[1]/span').text
        typeoforder = driver.find_element(
            By.CSS_SELECTOR,
            'body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-2 > div > a.list-group-item.active'
        ).text
        logging.info( f'Type of order -> {typeoforder}')
        time.sleep(2)

        # to check 'No_records_found' text is found or not
        no_gst_orders = False
        new_data = False
        try:
            
            no_gst_orders = driver.find_element(
                By.CSS_SELECTOR,
                'body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div:nth-child(2) > table' #error here
            ).is_displayed()
            # body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div:nth-child(4) > table

            logging.debug(
                f'\"No orders found\" message is there -> {no_gst_orders}'
            )
        except Exception as e:
            logging.error(e)

        
        # order table exist
        if not no_gst_orders:

            order_number = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[2]/span'
            ).text

            logging.debug(
                f'Order number = {order_number}'
            )
            # body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div.rettbl-format > div > table > tbody > tr > td:nth-child(2)
            order_date = driver.find_element(
                By.CSS_SELECTOR,
                'body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div.rettbl-format > div > table > tbody > tr > td:nth-child(3) > span'
            ).text
            
            cnf_order_date = datetime.strptime( order_date, "%d/%m/%Y" ).strftime( '%Y-%m-%d')
            logging.debug(
                f'Order type = {typeoforder}'
            )
            logging.debug(
                f'Order date = {order_date}'
            )
            logging.debug(
                f'Confirm Order date = {cnf_order_date}'
            )

            table_body = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table'
            )

            entries = table_body.find_elements(By.TAG_NAME,'tr')

            order_counts = table_body.find_elements(By.TAG_NAME,'a')

            logging.debug( f'count of links in table : {order_counts}')
            # Get active element from 'Order' table

            # atrr = driver.switch_to.active_element.get_attribute()
            try:
                sql = "select order_num, attachment from notice_download_gst_order_dot where client_id='%s' and order_num='%s' and ref_id='%s' " % (id, order_number,refid)
                mycursor.execute(sql)
                # Fetch all the rows in a list of lists.
                order_result = mycursor.fetchall()
                logging.debug( f'notice_download_gst_order : {len(order_result)}' )

            except Exception as e:
                logging.error( e)

            file_list = []
            
            for i in range(1, len(order_counts)+ 1):

                #print(notice_name)
                order_name = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[4]/span[%s]/p/a'
                    % (i)).text

                if len(order_result) == 0 :

                    # download notice
                    download = driver.find_element(
                        By.XPATH,
                        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[4]/span[%s]/p/a' % (i)
                    )
                    download.click()
                    file_list.append(order_name)
                    new_data = True
                    logging.info(f'DOT {order_name} order is downloaded')
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
            
                if len(order_result) < len(order_counts) and len(order_result) > 0 :
                    logging.debug('some data are available')
                    def order_exist():
                        logging.debug('start exist function')
                        for i in order_result:
                            logging.debug('checking current order file')
                            if i[1] ==  order_name:
                                return True
                        return False
                
                    # download order
                    logging.debug(f'exist function returned {order_exist()}')
                    if not order_exist():
                        logging.debug('exist if block start')
                        download = driver.find_element(
                            By.XPATH,
                            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[4]/span[%s]/p/a' % (i)
                        )
                    
                        download.click()
                        file_list.append(order_name)
                        new_data = True
                        # logging.info('line no 928')
                        logging.info(f'DOT {order_name} order is downloaded')
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[0])

                        time.sleep(1)
                    else:
                        logging.debug('order is already present.' )
            time.sleep( 1)
            if len(order_result) != len(order_counts): monitor_download_progress(dir_path, len(order_counts) if len(order_result) == 0 else len(order_counts) - len(order_result) )
            if len(file_list) > 0:
                for i in file_list:
                    try:
                        logging.debug('In try block' )
                        mycursor.execute(
                            "INSERT INTO notice_download_gst_order_dot (client_id, order_type, attachment, order_num, order_date, status, ref_id) VALUES(%s, %s,%s,%s,%s,%s,%s)",
                            (id,typeoforder,i,order_number,cnf_order_date, status, refid )
                        )
                        mydb.commit()
                    except Exception as e:
                        logging.error( e)
            mycursor.execute("INSERT INTO determination_of_tax (client_id, category, type, reference_or_order_num, order_date,   status, attachment) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                             (id, "Order", typeoforder, order_number, cnf_order_date, status, json.dumps(file_list))
                             ) 
            
            mydb.commit()
            logging.debug(f'last row added id in dot table - ${mycursor._last_insert_id}')
            driver.back()
        else:
            # No GST order notice
            time.sleep( 1)
            driver.back()
        

    except Exception as e:
        logging.error(e)
        time.sleep( 1)
        driver.back()
    return new_data

def intimation(id :int, refid : str, driver, dir_path :str):
    intimation_table_length = len(
    driver.find_elements(By.XPATH,
    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr'        ))
    # intimation_table=driver.find_elements(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr')
    logging.info( '------------------------------------------------------------------' )
    logging.info('Intimation Table')
    logging.info('------------------------------------------------------------------')
    logging.debug(f'length of the table={intimation_table_length}' )
    
    new_data = False
    if intimation_table_length > 0:
        logging.debug('start Intimation section')
        logging.debug(f'user id:{id}')
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/table/tbody/tr/td for 'No Records Found' message
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/table/tbody
    
        i_noticetype = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[1]/span'
        ).text
        i_ref = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[2]/span'
        ).text
        i_issue_date = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[3]/span'
        ).text
        i_due_date = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[4]/span'
        ).text
        i_section = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[5]/span'
        ).text

        i_cnf_issue_date = datetime.strptime( i_issue_date, "%d/%m/%Y" ).strftime( '%Y-%m-%d')
        i_cnf_due_date = datetime.strptime( i_due_date, "%d/%m/%Y" ).strftime( '%Y-%m-%d')

        logging.debug(f'intimation ={i_noticetype}')
        logging.debug( f'intimation refrence={i_ref}')
        logging.debug(f'intimation issue date={i_issue_date}')
        logging.debug(f'intimation Due Date={i_due_date}')
        logging.debug( f'intimation Section={i_section}')
        logging.debug( f'converted issue date={i_cnf_issue_date}')
        logging.debug( f'converted due date={i_cnf_due_date}')

        status = "Not Started"

        table_body = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody'
        )

        intimation_counts = table_body.find_elements(By.TAG_NAME,'a')

        logging.debug(
            f'count of links in table : {intimation_counts}'
        )
    
        try:
            sql = "select reference,notice_name from notice_download_gst_intimation where client_id='%s' and reference='%s' and ref_id='%s' " % (
                id,i_ref, refid)
            mycursor.execute( sql)
            # Fetch all the rows in a list of lists.
            intimation_result1 = mycursor.fetchall()
            logging.debug(  intimation_result1 )

        except Exception as e:
            logging.debug( e)

        file_list = []
        
        for i in range(1,len(intimation_counts) + 1):

            
            i_notice_name = driver.find_element(
                    By. XPATH,
                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span[%s]/p/a'% (i)
                ).text        
            #  here
            # if result is empty
            if len(intimation_result1) == 0  :
                

                # if gst_other_notice_result[0]['notice_name'] !=  n_notice_name:
                # download notice
                download = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span[%s]/p/a'
                    % (i)
                )
                
                download.click()
                file_list.append(i_notice_name)
                logging.info(f'{i_notice_name} is downloaded')
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                new_data = True
                time.sleep(1)
            
            # if result has some data
            if len(intimation_result1) < len(intimation_counts) and len(intimation_result1) > 0 :
                logging.debug('some data are available')
                def exist():
                    logging.debug('start exist function')
                    for i in intimation_result1:
                        logging.debug('checking current notice file')
                        if i[1] ==  i_notice_name:
                            return True
                    return False

                # download notice
                logging.debug(f'exist function returned {exist()}')
                if not exist():
                    logging.debug('exist if block start')
                    download = driver.find_element(
                        By.XPATH,
                        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span[%s]/p/a'
                        % (i)
                    )
                
                    download.click()
                    file_list.append(i_notice_name)
                    # logging.info('line no 928')
                    logging.info(f'{i_notice_name} is downloaded')
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    new_data = True
                    time.sleep(1)
                else:
                    logging.debug('notice is already present.' )
        if len(intimation_result1) != len(intimation_counts): monitor_download_progress(dir_path, len(intimation_counts) if len(intimation_result1) == 0 else len(intimation_counts) - len(intimation_result1) )
        if len(file_list) > 0:
            for i in file_list:
                try:
                    logging.debug('In try block' )
                    mycursor.execute(
                        "INSERT INTO notice_download_gst_intimation(client_id,notice_type,notice_name,reference,issue_date,due_date,section,status, ref_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (id, i_noticetype ,i , i_ref,i_cnf_issue_date, i_cnf_due_date, i_section,status, refid ))
                    mydb.commit()
                except Exception as e:
                    logging.error(e)
                    
        mycursor.execute("INSERT INTO scrutiny_of_returns (client_id, category, type, reference_or_order_num, issue_date, due_date, section , status, attachment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (id,"Intimation",i_noticetype, i_ref, i_cnf_issue_date, i_cnf_due_date, i_section, status, json.dumps(file_list))
                         )
        mydb.commit()
        logging.debug(f'last row inserted id in scrutiny of return table - {mycursor._last_insert_id}')
    return new_data


def notice(id :int, refid : str, driver, dir_path: str):
    logging.debug(f'user id:{id}')
    try:
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody
        #Click On Notice Tab
        driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[1]'
        ).click()
        
        notice_table = driver.find_elements(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr'
        )
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[1]/p/a
        logging.debug( f'Notice Table Length ###### = {len(notice_table)}')
        
        n_noticetype = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[1]/span'
        ).text
        n_ref = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[2]/span'
        ).text
        n_issue_date = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[3]/span'
        ).text
        n_due_date = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[4]/span'
        ).text
        person_hearing = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[5]/span/span'
        ).text
        
        n_section = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[6]/span'
        ).text

        n_cnf_issue_date = datetime.strptime(  n_issue_date,  "%d/%m/%Y").strftime('%Y-%m-%d')
        n_cnf_due_date = datetime.strptime( n_due_date,    "%d/%m/%Y" ).strftime('%Y-%m-%d')
        status = "Not Started"

        logging.debug(f'n notice type : {n_noticetype}')
        logging.debug(f'n  n refrence: {n_ref}')
        logging.debug( f'n issue date : {n_issue_date}')
        logging.debug( f'n Due Date : {n_due_date}')
        logging.debug(f'n Section : {n_section}')
        logging.debug(f'n Personal Hearing : {person_hearing}' )
        logging.debug( f'n converted issue date : {n_cnf_issue_date}')
        logging.debug( f'converted due date : {n_cnf_due_date}')
        
        table_body = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody'
        )
        entries = table_body.find_elements(By.TAG_NAME, 'tr')

        notice_counts = table_body.find_elements( By.TAG_NAME, 'a')

        logging.debug( f'count of links in table : {len(notice_counts)}')
        
        try:
            sql = "select reference,notice_name from notice_download_gst_other_notice where client_id='%s' and reference='%s' and ref_id='%s' " % (
                id, n_ref, refid)
            mycursor.execute( sql)
            # Fetch all the rows in a list of lists.
            gst_other_notice_result = mycursor.fetchall()
            for row in gst_other_notice_result:
                refernce = row[ 0]
                notice_name = row[1]
            logging.debug(f'gst notices table count : {len(gst_other_notice_result)}')
            logging.debug(f'gst notices table : {gst_other_notice_result}')
        except Exception as e:
            logging.debug(e)
        file_list = []
        new_data = False
        for i in range( 1, len(notice_counts) + 1):

            #print(notice_name)
        
            # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[1]/p/a
            n_notice_name = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[%s]/p/a'
                % (i)).text

            # if result is empty
            if len(gst_other_notice_result) == 0  :

                # download notice
                download = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[%s]/p/a'
                    % (i)
                )
                download.click()
                file_list.append(n_notice_name)
                logging.info(f'{n_notice_name} notice is downloaded')
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                new_data = True
                time.sleep(1)

            # if result has some data
            if len(gst_other_notice_result) < len(notice_counts) and len(gst_other_notice_result) > 0 :
                logging.debug('some data are available')
                def notice_exist1():
                    logging.debug('start exist function')
                    for i in gst_other_notice_result:
                        logging.debug('checking current notice file')
                        if i[1] ==  n_notice_name:
                            return True
                    return False
                    
                # download notice
                logging.debug(f'exist function returned {notice_exist1()}')
                if not notice_exist1():
                    logging.debug('exist if block start')
                    download = driver.find_element(
                        By.XPATH,
                        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td[9]/span[%s]/p/a'
                        % (i)
                    )
                    download.click()
                    file_list.append(n_notice_name)
                    new_data = True
                    logging.info(f'{n_notice_name} is downloaded')
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)

                else:
                    logging.debug('notice is already present.' )
        time.sleep(1)
    
        if len(gst_other_notice_result) != len(notice_counts): monitor_download_progress(dir_path, len(notice_counts) if len(gst_other_notice_result) == 0 else len(notice_counts) - len(gst_other_notice_result) )
        if len(file_list) > 0:
            for i in file_list:
                try:
                    logging.debug('In try block' )
                    mycursor.execute(
                        "INSERT INTO notice_download_gst_other_notice(client_id,notice_type,notice_name,reference,issue_date,due_date,section,personal_hearing,status,ref_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (id, n_noticetype, i, n_ref, n_cnf_issue_date, n_cnf_due_date, n_section,  person_hearing, status, refid ) )
                    mydb.commit()
                except Exception as e:
                    logging.error(e)
        logging.info(f'notice list - {file_list}')
        # client_id, category, type, reference_or_order_num, issue_date due_date section personal_hearing status attachment
        mycursor.execute("INSERT INTO scrutiny_of_returns (client_id, category, type, reference_or_order_num, issue_date, due_date, section , personal_hearing, status, attachment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (id,"Notice",n_noticetype, n_ref, n_cnf_issue_date, n_cnf_due_date, n_section, person_hearing, status, json.dumps(file_list))
                         )
        mydb.commit()
        logging.debug(f'last row inserted id in scrutiny of return table - {mycursor._last_insert_id}')

    except Exception as e:
        logging.error(e)
    logging.debug('notice tab section end here')
    time.sleep(2)
    return new_data

def order(id :int,refid : str, driver, dir_path: str):
    logging.debug(f'user id:{id}')
    try:
        # In the order tab
        status = "Not Started"
        time.sleep(2)
        logging.debug('order tab selected')
        logging.debug('In try block')
        # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[3]
        
        # driver.quit()

        # typeoforder=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[1]/span').text
        typeoforder = driver.find_element(
            By.CSS_SELECTOR,
            'body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-2 > div > a.list-group-item.active'
        ).text
        logging.info( f'Type of order -> {typeoforder}')
        time.sleep(2)

        # to check 'No_records_found' text is found or not
        no_gst_orders = False
        try:
            
            no_gst_orders = driver.find_element(
                By.CSS_SELECTOR,
                'body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div:nth-child(2) > table' #error here
            ).is_displayed()
            # body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div:nth-child(4) > table

            logging.debug(
                f'\"No orders found\" message is there -> {no_gst_orders}'
            )
        except Exception as e:
            logging.error(e)

        new_data = False
        # order table exist
        if not no_gst_orders:

            order_number = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[2]/span'
            ).text

            logging.debug(
                f'Order number = {order_number}'
            )
            # body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div.rettbl-format > div > table > tbody > tr > td:nth-child(2)
            order_date = driver.find_element(
                By.CSS_SELECTOR,
                'body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div.rettbl-format > div > table > tbody > tr > td:nth-child(3) > span'
            ).text
            
            cnf_order_date = datetime.strptime( order_date, "%d/%m/%Y" ).strftime( '%Y-%m-%d')
            logging.debug(
                f'Order type = {typeoforder}'
            )
            logging.debug(
                f'Order date = {order_date}'
            )
            logging.debug(
                f'Confirm Order date = {cnf_order_date}'
            )

            table_body = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table'
            )

            entries = table_body.find_elements(By.TAG_NAME,'tr')

            order_counts = table_body.find_elements(By.TAG_NAME,'a')

            logging.debug( f'count of links in table : {order_counts}')
            # Get active element from 'Order' table

            # atrr = driver.switch_to.active_element.get_attribute()
            try:
                sql = "select order_number, order_name from notice_download_gst_order where client_id='%s' and order_number='%s' and ref_id='%s' " % (id, order_number,refid)
                mycursor.execute(sql)
                # Fetch all the rows in a list of lists.
                order_result = mycursor.fetchall()
                logging.debug( f'notice_download_gst_order : {order_result}' )

            except Exception as e:
                logging.error( e)

            file_list = []
            
            for i in range(1, len(order_counts)+ 1):
                
                #print(notice_name)
                order_name = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[4]/span[%s]/p/a'
                    % (i)).text

                if len(order_result) == 0 :

                    # download notice
                    download = driver.find_element(
                        By.XPATH,
                        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[4]/span[%s]/p/a' % (i)
                    )
                    
                    download.click()
                    file_list.append(order_name)
                    logging.info(f'{order_name} is downloaded')
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    new_data = True
                    time.sleep(1)

                    logging.debug( order_name )
                    time.sleep(1)
            
                if len(order_result) < len(order_counts) and len(order_result) > 0 :
                    logging.debug('some data are available')
                    def order_exist():
                        logging.debug('start exist function')
                        for i in order_result:
                            logging.debug('checking current order file')
                            if i[1] ==  order_name:
                                return True
                        return False
                
                    # download order
                    logging.debug(f'exist function returned {order_exist()}')
                    if not order_exist():
                        logging.debug('exist if block start')
                        download = driver.find_element(
                            By.XPATH,
                            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td[4]/span[%s]/p/a' % (i)
                        )
                    
                        download.click()
                        file_list.append(order_name)
                        new_data = True
                        logging.info(f'{order_name} is downloaded')
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)

                        logging.debug( order_name)
                        time.sleep(1)
                    else:
                        logging.debug('order is already present.' )
            time.sleep( 1)
            if len(order_result) != len(order_counts): monitor_download_progress(dir_path, len(order_counts) if len(order_result) == 0 else len(order_counts) - len(order_result) )
            if len(file_list) > 0:
                for i in file_list:
                    try:
                        logging.debug('In try block' )
                        mycursor.execute(
                            "INSERT INTO notice_download_gst_order(client_id, order_type, order_name, order_number, order_date, status, ref_id) VALUES(%s, %s,%s,%s,%s,%s,%s)",
                            (id, typeoforder, i, order_number, cnf_order_date, status, refid )
                        )
                        mydb.commit()
                    except Exception as e:
                        logging.error(e)
            mycursor.execute("INSERT INTO scrutiny_of_returns (client_id, category, type, reference_or_order_num, order_date,   status, attachment) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                             (id, "Order", typeoforder, order_number, cnf_order_date, status, json.dumps(file_list))
                             ) 
            
            mydb.commit()
            logging.debug(f'last row added id in dot table - ${mycursor._last_insert_id}')
            driver.back()
        else:
            # No GST order notice
            time.sleep( 1)
            driver.back()

    except Exception as e:
        logging.error(e)
        time.sleep( 1)
        driver.back()
    return new_data
    
def user_logout(driver):
    logging.debug('user is going to logout')
    time.sleep(2)
    driver.find_element(
        By.XPATH,
        '/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li/div/a'
    ).click()
    time.sleep(2)
    driver.find_element(
        By.XPATH,
        '/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li[1]/div/ul/li[5]/a'
    ).click()
    time.sleep(2)
    driver.find_element(
        By.XPATH,
        '/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li/a'
    ).click()
    driver.quit()

def upload_data(dir_path : str, file_type : str):
    s3_client = boto3.client('s3',aws_access_key_id='AKIAX2MHZPD6X6YQ2C5B',aws_secret_access_key='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',region_name='ap-south-1')
    
    items = os.listdir( dir_path)
    if len(items) > 0:
        sort_list = sorted(items)
        logging.info(sort_list)
        for item in sort_list:
            i = dir_path+"/"+item
            logging.info(f'{i} file path')
            data = open(dir_path+"/"+item,  'rb')
            # s3_client.Bucket('demo-patronaid').put_object( Key=file_type+'/'+item , Body=data)
            s3_client.upload_file(Filename=i, Bucket="demo-patronaid", Key=file_type+'/'+item)
            logging.info(f'{item} has been uploaded successfully!')
        for file in os.listdir(dir_path):
            try:
                os.remove(os.path.join(dir_path, file))
                logging.info(f"File {file} has been deleted from local directory")
            except Exception as e:
                logging.error(e)
    time.sleep(2)

def monitor_download_progress(download_dir:str,  fileCount:int):
    
    logging.info('monitoring download progress...')
    while True:
        items = [ i for i in os.listdir( download_dir ) if True is i.endswith(".pdf") ]
        logging.debug(f"files in current folder - {items}")
        if len( items ) >= fileCount :
            logging.debug(f'more than {fileCount} items')
            break
        else:
            logging.debug(f'less than {fileCount} ')
        time.sleep(1)
    
def start_gst():
    flg = '222'
    sql = "select * from notice_download_gst_clients where flag='%s'" % (flg)
    # driver.get('https://eportal.incometax.gov.in/iec/foservices/#/login')
    try:
        # Execute the SQL command
        mycursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = mycursor.fetchall()
        number_of_rows = len(results)
        # print(number_of_rows)
        l = len(results)
        cnt = l

        if l == 0:
            messagebox.showerror(
                'Error',
                'Please select client for download notices/intimations')

        # if cnt==0:
        for row in results:
            if cnt > 0:
                # print("In if condition")
                name = row[1]
                username =  base64.b64decode(row[2]).decode()
                password = base64.b64decode(row[3]).decode() 
                id = row[0]
                name = 'G' + str(row[0])
                logging.debug(f'id={id}')
                logging.debug(f'name={name}')
                logging.debug(f'username={username}')
                logging.debug(f'password={password}')

                # new_dir = "/home/rdpuser/ca/gst_notice/"+name
                #new_dir="D:\patronaid projects\projects\RPA Online\\notice_management\static\All_Notice\GST\\"+name
                #new_dir="/var/www/html/django/assets/GST/"+name
                # new_dir="c:\patronaid\GST\\"+name
                # new_dir = "C:\patronaid\GST\\" + name
                new_dir="/Users/tejas/Selenium/Assessment_management/gst_notice/"+name
                # new_dir+=name
                def gst_start():
                    logging.info("GST function started...")
                    prefs = {
                        "download.default_directory" : new_dir,
                        "credentials_enable_service":False,
                        "profile.password_manager_enabled":False,
                        "profile.default_content_setting_values_notifications":False
                    }

                    option.add_experimental_option("prefs", prefs)

                    option.add_argument("start-maximized")
                    # option.add_experimental_option("prefs", {"download.default_directory" : "/Users/tejas/Selenium/GST/inputs"})
                    option.add_argument('disable-features=DownloadUI')
                    option.add_experimental_option("excludeSwitches",["enable-automation"])
                    option.add_experimental_option('useAutomationExtension',False)
                    option.add_argument( '--disable-blink-features=AutomationControlled')
                    # driver = webdriver.Chrome(service=ChromeService(
                        # (ChromeDriverManager().install())),options=option)
                    driver = uc.Chrome(options=option, headless=False)
                    driver.maximize_window()

                    try:

                        driver.get(
                            'https://services.gst.gov.in/services/login')
                        time.sleep(3)

                        usernameClick = driver.find_element(
                            By.XPATH, '//*[@id="username"]')
                        usernameClick.send_keys(username)

                        passwordClick = driver.find_element(
                            By.XPATH, '//*[@id="user_pass"]')
                        passwordClick.send_keys(password)
                        time.sleep(5)
                        read_captcha = driver.find_element(By.XPATH,'//*[@id="imgCaptcha"]')
                        read_captcha.screenshot('captcha.png')
                        time.sleep(5)
                        solver = imagecaptcha()
                        solver.set_verbose(1)
                        solver.set_key("41b4ba9feb34f95f806ce53143481620")
                        
                        
                        # Specify softId to earn 10% commission with your app.
                        # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
                        solver.set_soft_id(0)

                        captcha_text = solver.solve_and_return_solution("captcha.png")
                        if captcha_text != 0:
                            print("captcha text "+captcha_text)
                            logging.info('Enter the captcha by the user')
                            captch_insert = driver.find_element(By.XPATH,'//*[@id="captcha"]')
                            captch_insert.click()
                            driver.find_element(By.XPATH,'//*[@id="captcha"]').send_keys(captcha_text)
                        else:
                            print("task finished with error "+solver.error_code)
                        
                        
                        # locator = driver.find_element(By.CSS_SELECTOR,".btn").click()
                        try:
                            wait = WebDriverWait(
                                driver, 10)  # 10 seconds maximum wait time
                            button = wait.until(
                                EC.element_to_be_clickable((
                                    By.XPATH,
                                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/form/div[6]/div/button'
                                )))
                            button.click()
                            
                            # invalid_login = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div/div/div/alert-message/div').is_displayed()
                            # if invalid_login:
                                # messagebox.showerror('')
                                # driver.quit()
                                
                            time.sleep(5)
                        except Exception as e:
                            logging.error(e)
                            driver.quit()
                        time.sleep(1)
                        
                        # minimize chrome window
                        # driver.minimize_window()
                        try:
                            driver.find_element(
                                By.XPATH,
                                '//*[@id="adhrtableV"]/div/div/div[2]/a[2]'
                            ).click()
                            time.sleep(3)
                            driver.find_element(
                                By.XPATH,
                                '//*[@id="caNumpopupV"]/div/div/div[2]/a[2]'
                            ).click()
                        except:
                            pass
                    
                        # Show "Core business selection" dialog box
                        try:
                            core_business = driver.find_element(By.XPATH, '//*[@id="exampleModalCenterTitle"]').is_displayed()
                            if core_business:
                                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        except Exception as e:
                            logging.error(e)
                        # shown prompt 1
                        time.sleep(2)
                        try:
                            driver.find_element(
                                By.XPATH,
                                '//*[@id="adhrtableV"]/div/div/div[2]/a[2]'
                            ).click() # //*[@id="adhrtableV"]/div/div/div[2]/a[2]
                            logging.debug('clicked first prompt')
                        except Exception as e:
                            logging.error(e)
                            time.sleep(4)

                        # shown prompt 2
                        try:
                            driver.find_element( By.XPATH,'//*[@id="caNumpopupV"]/div/div/div[2]/a[2]'
                            ).click()
                            logging.debug('clicked second prompt')
                        except Exception as e:
                            logging.error(e)
                        # /html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/div/div/div/ul/li[1]/a
                        # /html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/div/div/div/ul/li[2]/a 
                        # html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/div/div/div/ul/li[3]/a
                        time.sleep(5)
                        driver.find_element(
                            By.XPATH, '//*[@id="main"]/ul/li[2]/a').click()
                        time.sleep(5)

                        driver.find_element(
                            By.XPATH,
                            '//*[@id="main"]/ul/li[2]/ul/li[6]/div/a').click()
                        time.sleep(4)
                        driver.find_element(
                            By.XPATH,
                            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/ul/li[4]/a'
                        ).click()
                        time.sleep(5)
                        page_len = 3
                        try:
                            is_pagination = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/div/div/div/ul/li').is_displayed()
                            if is_pagination:
                                page_len = len(driver.find_elements(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/div/div/div/ul/li'))
                                logging.debug(f'pagination length - {page_len}')
                            # driver.quit()
                        except Exception as e:
                            logging.error(e)
                        
                        # driver.find_element(By.XPATH,'//*[@id="main"]/ul/li[2]/ul/li[6]/ul/li[4]/a').click()
                        time.sleep(2)
                        divlen = 0
                        
                        logging.debug(f'for loop length - {(page_len - 2) + 1}')
                        for i in range(1 , (page_len - 2) + 1):
                            logging.debug('pagination loop')
                            time.sleep(1)
                            logging.debug(f'Iteration index - {i}')
                            tablelen = driver.find_elements(
                                By.XPATH,
                                '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr'
                            )

                            divlenght = len(tablelen)

                            logging.debug(f'div-length ={divlenght}')

                            try:
                                divlen = divlenght
                                logging.debug(divlen)
                            except Exception as e:
                                logging.error(e)
                            if (divlen > 0): 
                                # /html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr[10]
                                for i in range(1, divlenght + 1):

                                    # /html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr[1]/td[8]/div/a

                                    dynamic_xpath = '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr[' + str(
                                        i) + ']/td[8]/div/a'
                                    dynamic_notice_xpath = '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr[' + str(
                                        i) + ']/td[1]/div'
                                    # print(dynamic_xpath)
                                    time.sleep(1)

                                    try:
                                        notice_name = driver.find_element(
                                            By.XPATH, dynamic_notice_xpath).text
                                        logging.info('----------------------------------------')
                                        logging.info(f'website notice name={notice_name}')
                                        logging.info('----------------------------------------')

                                        issuedatexpath = '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr[' + str(
                                            i) + ']/td[5]'
                                        issue_date = driver.find_element(
                                            By.XPATH, issuedatexpath).text
                                        logging.info(
                                            '----------------------------------------'
                                        )
                                        logging.info(f'Issue date={issue_date}')
                                        logging.info(
                                            '----------------------------------------'
                                        )
                                        cnf_issue_date1 = datetime.strptime(
                                            issue_date,
                                            "%d/%m/%Y").strftime('%Y-%m-%d')

                                        issuebyxpath = '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/table/tbody/tr[' + str(
                                            i) + ']/td[2]'
                                        issue_by = driver.find_element(
                                            By.XPATH, issuebyxpath).text
                                        logging.info( '----------------------------------------' )
                                        logging.info(f'Issue by={issue_by}')
                                        logging.info( '----------------------------------------')
                                        # print(i)
                                        # driver.close()

                                        #--------------------- Fetch Notice name from database -----------------------------
                                        try:
                                            sql = "select notice_name from notice_download_gst_notice where client_id='%s' and notice_name='%s'" % (
                                                id, notice_name)
                                            mycursor.execute(sql)
                                            # Fetch all the rows in a list of lists.
                                            result = mycursor.fetchall()
                                            logging.info('----------------------------------------')
                                            logging.info(
                                                f'Select query result before 1st table notice download ={result}'
                                            )
                                            logging.info( '----------------------------------------')
                                        except Exception as e:
                                            logging.info('---------------- ------------------------')
                                            logging.error(e)
                                            logging.info('----------------------------------------')

                                        if not result:

                                            try:
                                                logging.debug('In try block')
                                                driver.find_element(
                                                    By.XPATH,
                                                    dynamic_xpath).click()
                                                logging.debug(f'File {notice_name} notice is downloaded successfully!')
                                                try:
                                                    driver.switch_to.window(
                                                        driver.window_handles[0])
                                                    time.sleep(5)
                                                    driver.switch_to.window(
                                                        driver.window_handles[1])
                                                    time.sleep(1)
                                                    driver.close()
                                                    driver.switch_to.window(
                                                        driver.window_handles[0])
                                                except Exception as e:
                                                    logging.error(e)
                                                status = 'Not Started'

                                                mycursor.execute(
                                                    "INSERT INTO notice_download_gst_notice (client_id,notice_name,issue_date,issue_by,status) VALUES(%s,%s,%s,%s,%s)",
                                                    (id, notice_name,cnf_issue_date1,issue_by,status))
                                                mydb.commit()
                                                
                                            except Exception as e:
                                                logging.error(e.with_traceback)
                                            # upload files to s3 bucket
                                            upload_data(new_dir, '/GST/'+name+'/Notice and Orders')

                                        time.sleep(1)
                                        divlen = divlen - 1
                                        logging.info('----------------------------------------')
                                        logging.debug(divlen)

                                        
                                    except:
                                        flag = 0
                                        try:

                                            logging.debug(username)
                                            Update = "Update notice_download_gst_clients set flag='%s' where username='%s'" % (
                                                flag, username)
                                            mycursor.execute(Update)
                                            mydb.commit()
                                        except Exception as e:
                                            logging.debug("In exception of first main try")
                                            logging.error(e)
                            
                            # click on the next pagination number
                            try: #/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/div/div/div/ul/li[4]
                                driver.find_element(
                                    By.XPATH,
                                    f'/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[7]/div/div/div/div/div/ul/li[{page_len}]/a'
                                ).click()
                                time.sleep(1)
                            except Exception as e:
                                logging.error(e)
                            # driver.quit()
                        else:
                            logging.error('Something goes wrong')
                        
                        
                        # view notices/orders table is empty
                        if (divlen == 0):

                            time.sleep(1)
                            driver.find_element(
                                By.XPATH,
                                '//*[@id="main"]/ul/li[2]/a').click()
                            #
                            try:
                                # go to Additional notices and order section
                                logging.info('In try block')

                                time.sleep(2)

                                try:
                                    user_services = driver.find_element(
                                        By.LINK_TEXT, 'User Services')
                                    logging.debug('user_services captured')

                                    time.sleep(1)
                                    action = ActionChains(driver)

                                    # mouse hover on the 'User Services' menu
                                    action.move_to_element(
                                        user_services).perform()
                                    logging.debug(
                                        'mouse hovered on the user services menu'
                                    )

                                    view_additional_sub_menu = driver.find_element(
                                        By.LINK_TEXT,
                                        'View Additional Notices/Orders')
                                    logging.debug(
                                        'view additional notices/orders captures'
                                    )
                                    time.sleep(1)

                                    # click on the 'View additional notices / orders' sub-menu
                                    action.move_to_element(
                                        view_additional_sub_menu).click(
                                        ).perform()
                                    time.sleep(3)
                                    logging.debug(
                                        'mouse clicked on the view additional notices/orders sub menu'
                                    )

                                    time.sleep(2)
                                except Exception as e:
                                    logging.error(f'Exception -> {e}')

                                # driver.quite()

                                time.sleep(1)

                                # clicked on 100 number
                                try:
                                    driver.find_element(
                                        By.XPATH,
                                        '//*[@id="table1"]/div/div/div/div/div/div/div/button[4]/span'
                                    ).click()
                                except Exception as e:
                                    logging.error(e)

                                # get count of table rows of Additional notices & orders
                                countRows = driver.find_elements(
                                    By.XPATH,
                                    '//*[@id="table1"]/div/div/div/table/tbody/tr'
                                )
                                cnts = len(countRows)
                                # cntrowss=len(countRows)
                                logging.debug('count rows: ' + str(len(countRows)))

                                for i in range(1, cnts + 1):

                                    # xpath of view visit in each row
                                    # for row in len(countRows) :

                                    logging.debug('########## cnts ##################' )
                                    logging.debug(f'counter -> {cnts}')

                                    time.sleep(2)

                                    # Read the row data in the Additional Notices and Orders
                                    typeofnotice = driver.find_element(
                                        By.XPATH,
                                        '//*[@id="table1"]/div/div/div/table/tbody/tr[%s]/td[1]/span'
                                        % (i)).text
                                    description = driver.find_element(
                                        By.XPATH,
                                        '//*[@id="table1"]/div/div/div/table/tbody/tr[%s]/td[2]/span'
                                        % (i)).text
                                    ref = driver.find_element(
                                        By.XPATH,
                                        '//*[@id="table1"]/div/div/div/table/tbody/tr[%s]/td[3]/span'
                                        % (i)).text
                                    issue_date1 = driver.find_element(
                                        By.XPATH,
                                        '//*[@id="table1"]/div/div/div/table/tbody/tr[%s]/td[4]/span'
                                        % (i)).text

                                    logging.info('---------------------------------')
                                    logging.info(f'Type of notice={typeofnotice}')
                                    logging.info('---------------------------------')
                                    logging.info( f'Description={description}')
                                    logging.info( '---------------------------------')
                                    logging.info(f'Reference Id={ref}')
                                    logging.info('---------------------------------')
                                    logging.info(
                                        f'Date of Issuance={issue_date1}')

                                    driver.find_element(
                                        By.XPATH,
                                        '//*[@id="table1"]/div/div/div/table/tbody/tr['
                                        + str(i) + ']/td[5]/a').click()
                                    cnts = cnts - 1

                                    time.sleep(4)

                                    if "SCRUTINY OF RETURNS" == typeofnotice:
                                        tabs = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a')
                                        logging.debug(f'tab length: {len(tabs)}')
                                                    
                                        for i in range(1, len(tabs)+1 ):
                                            tab_title = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[{i}]').text
                                            if tab_title == 'INTIMATIONS':
                                                driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[{i}]').click()
                                            
                                                isData = intimation(id, ref, driver, new_dir)
                                                # upload files to s3 bucket
                                                if isData : upload_data(new_dir, '/GST/'+name+'/SOR/Intimation')
                                                time.sleep(1)
                                            if tab_title == 'NOTICES':
                                                logging.info('Notice Table')
                                                driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[{i}]').click()
                                                logging.info('notice function to be called')
                                                isData = notice(id, ref,driver, new_dir)
                                                time.sleep(1)
                                                # upload files to s3 bucket
                                                if isData: upload_data(new_dir, '/GST/'+name+'/SOR/Notice')
                                                
                                            if tab_title == 'ORDERS':
                                                logging.info('Order Table')
                                                driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[{i}]').click()
                                                logging.info('order function to be called')
                                                isData = order(id, ref, driver, new_dir)
                                                # upload files to s3 bucket
                                                if isData: upload_data(new_dir, '/GST/'+name+'/SOR/Order')

                                        time.sleep(3)
                                        # clicked on 100 number
                                        try:
                                            driver.find_element(
                                                By.XPATH,
                                                '//*[@id="table1"]/div/div/div/div/div/div/div/button[4]/span'
                                            ).click()
                                        except Exception as e:
                                            logging.error(e)
                                        
                                    else:
                                        if typeofnotice == "APPEAL":
                                            logging.debug('In the Appeal section')
                                            
                                            try:
                                                # In the order tab
                                                status = "Not Started"
                                                time.sleep(2)
                                                logging.debug('order tab selected')
                                                logging.debug('In try block')
                                                # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[3]
                                                driver.find_element(
                                                    By.XPATH,
                                                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[4]'
                                                ).click()
                                                
                                                time.sleep(1)

                                                order_number = driver.find_element(
                                                    By.XPATH,
                                                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[4]/table/tbody/tr/td[1]'
                                                ).text

                                                logging.debug(
                                                    f'Order number = {order_number}'
                                                )
                                                # body > div.content-wrapper > div.container > div > div:nth-child(2) > div > div > div > div > div > div.col-md-10 > div > div > div.rettbl-format > div > table > tbody > tr > td:nth-child(2)
                                                order_date = driver.find_element(
                                                    By.XPATH,
                                                    '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[4]/table/tbody/tr/td[3]'
                                                ).text
                                                        
                                                cnf_order_date = datetime.strptime( order_date, "%d/%m/%Y" ).strftime( '%Y-%m-%d')
                                                # logging.debug( f'Order type = {typeoforder}')
                                                logging.debug(f'Order date = {order_date}' )
                                                logging.debug( f'Confirm Order date = {cnf_order_date}' )

                                                
                                                # Get active element from 'Order' table

                                                try:
                                                    sql = "select order_ref_or_num, documents from notice_download_gst_order_appeal where client_id='%s' and order_ref_or_num ='%s' and ref_id='%s' " % (id, order_number,ref)
                                                    mycursor.execute(sql)
                                                    # Fetch all the rows in a list of lists.
                                                    order_result = mycursor.fetchall()
                                                    logging.debug( f'notice_download_gst_order : {order_result}' )

                                                except Exception as e:
                                                    logging.error( e)

                                                # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/table/tbody/tr/td

                                                if len(order_result) == 0 :

                                                    order_name = driver.find_element(
                                                        By.XPATH,
                                                        '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[4]/table/tbody/tr/td[5]'
                                                    ).text
                                                    # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[4]/table/tbody/tr/td[5] /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[4]/table/tbody/tr/td[5]
                                                    # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[4]/table/tbody/tr/td[5]
                                                    time.sleep(2)
                                                    # download notice
                                                    try:
                                                        logging.debug('before click')
                                                        driver.find_element(
                                                            By.XPATH,
                                                            '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[4]/table/tbody/tr/td[5]/div[1]/a'
                                                        ).click()
                                                        logging.debug('after click')
                                                    except Exception as e:
                                                        logging.error(e)
                                                    
                                                    time.sleep(1)
                                                    driver.switch_to.window(driver.window_handles[0])
                                                    time.sleep(1)
                                                    monitor_download_progress(new_dir, 1)
                                                    # logging.info(f'Appeal order file -> {order_name} is downloaded successfully.')
                                                    try:
                                                        logging.debug('In try block' )
                                                        mycursor.execute(
                                                            "INSERT INTO notice_download_gst_order_appeal(client_id, order_ref_or_num, order_date, status, ref_id, documents) VALUES(%s, %s,%s,%s,%s,%s)",
                                                                        (id,order_number,cnf_order_date, status, ref, order_name )
                                                        )
                                                        mydb.commit()
                                                
                                                    except Exception as e:
                                                        logging.error(e)
                                                        
                                                    # logging.debug( order_name )
                                                    time.sleep(1)
                                                    # upload files to s3 bucket
                                                    upload_data(new_dir, '/GST/'+name+'/Appeal/Order')
                                                    # driver.quit()
                                                time.sleep( 1)
                                                driver.back()
                                                # else:
                                                #     # No GST order notice
                                                #     time.sleep( 1)
                                                #     driver.back()

                                            except Exception as e:
                                                logging.error(e)
                                                time.sleep( 1)
                                                driver.back()

                                                # get previous page and load Additional notices & orders table
                                            # driver.back()

                                            time.sleep(2)
                                            # clicked on 100 number
                                            driver.find_element(
                                                By.XPATH,
                                                '//*[@id="table1"]/div/div/div/div/div/div/div/button[4]/span'
                                            ).click()
                                        else:
                                            logging.debug('-----------------------------------')
                                            logging.debug( ' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> In the DETERMINATION OF TAX <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ')
                                            logging.debug( '-----------------------------------')

                                            time.sleep(1)
                                            tabs = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a')
                                            logging.debug(f'tab length: {len(tabs)}')
                                                    
                                            for i in range(1, len(tabs)+1 ):
                                                # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[1]
                                                driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[{i}]').click()
                                                tab_title = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/a[{i}]').text
                                                if tab_title == 'INTIMATIONS':
                                                    # /html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/table/tbody/tr
                                                    time.sleep(1)
                                                
                                                    isData = dot_intimation(id, ref, driver, new_dir)
                                                    # upload files to s3 bucket
                                                    if isData: upload_data(new_dir, '/GST/'+name+'/DOT/Intimation')
                                                if tab_title == 'NOTICES':
                                                    time.sleep(1)
                                                    logging.info('Notice Table')
                                                    
                                                    logging.info('notice function to be called')
                                                    isData = dot_notice(id, ref, driver, new_dir)
                                                    # upload files to s3 bucket
                                                    if isData: upload_data(new_dir, '/GST/'+name+'/DOT/Notice')
                                            
                                                if tab_title == 'ORDERS':
                                                    time.sleep(1)
                                                    logging.info('Order Table')
                                                    logging.info('order function to be called')
                                                    isData = dot_order(id, ref, driver, new_dir)
                                                    # upload files to s3 bucket
                                                    if isData: upload_data(new_dir, '/GST/'+name+'/DOT/Order')
                                                if tab_title == 'REPLIES':
                                                    time.sleep(1)

                                            time.sleep(2)
                                            # driver.back()
                                            time.sleep(2)
                                            # clicked on 100 number
                                            driver.find_element(
                                                By.XPATH,
                                                '//*[@id="table1"]/div/div/div/div/div/div/div/button[4]/span'
                                            ).click()
                                # user is going to logout
                                user_logout(driver)

                            except Exception as e:
                                # print(e, exc_info=True)
                                logging.error(e)
                                flag = 0
                                try:
                                    logging.info(f'username -> {username} has updated flag')
                                    Update = "Update notice_download_gst_clients set flag='%s' where username='%s'" % (
                                        flag, username)
                                    mycursor.execute(Update)
                                except Exception as e:
                                    logging.error(e)

                            logging.debug('Selenium script is done')

                    except Exception as e:

                        print("Expetion of windows open try")
                        logging.error(e)
                        logging.debug('flag updated to -1')
                        flag = 0
                        try:
                            print(username)
                            Update = "Update notice_download_gst_clients set flag='%s' " % (
                                flag)
                            mycursor.execute(Update)
                        except Exception as e:
                            logging.error(e)

                    finally:
                        # downloaded notices and after that flag will be reset to all clients
                        flag = -1
                        Update = "Update notice_download_gst_clients set flag='-1'"
                        mycursor.execute(Update)
                        logging.debug('flag updated to -1')
                        driver.quit()

                def updateflags():
                    try:
                        # downloaded notices and after that flag will be reset to all clients
                        Update = "Update notice_download_gst_clients set flag='-1'"
                        mycursor.execute(Update)
                        logging.debug('flag updated to -1')
                        mydb.commit()

                    except Exception as e:
                        print("Update flags exception")
                        logging.error(f'Update flags exception = {e}')

                try:
                    if os.path.exists(new_dir):
                        gst_start()

                        logging.debug('Gst start() exceuted')
                        updateflags()
                    else:
                        os.mkdir(new_dir)
                        gst_start()

                        logging.debug('Gst start() exceuted in else part')
                        updateflags()
                except Exception as e:
                    logging.error(e)

                try:
                    mydb.commit()
                    # driver.quit()
                    logging.info('Record updated')
                except:
                    pass
                    #Close the database connection
                    #mydb.close()
            else:
                messagebox.showinfo('Success','All notices are downloaded successfully')
                #mydb.close()

    except:
        Update = "Update notice_download_gst_clients set flag='-1'"
        mycursor.execute(Update)
        logging.debug('flag updated to -1')
        #mydb.close()


start_gst()

