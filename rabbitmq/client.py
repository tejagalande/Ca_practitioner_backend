import pika
import subprocess
import psutil
import time
import signal
import sys
import os

# Ox0000 for IT and Ox1111 for GST

# Callback function to handle received messages
ipid=None
def callback(ch, method, properties, body):
    

    #print(f" Received {body}")
   
    #ch.basic_ack(delivery_tag=method.delivery_tag)
 


    # print(body)
    # print(type(body))
    # print(body.decode("utf-8"))
    
    if body.decode("utf-8") == "Ox0000":
        
        print("[x] Income Tax service started now.....")
        script_path='C:\\Users\\assement\\income_tax\\income_tax.exe'
        subprocess.Popen(["start","cmd","/k",script_path],shell=True)
       
        print("process id",ipid)
    elif body.decode("utf-8") == "Ox1111":
         print("[x] GST service started now.....")
         #scr
         script_path='C:\\Users\\assement\\gst\\gst.exe'
         subprocess.Popen(["start","cmd","/c",script_path],shell=True)
    elif body.decode("utf-8") == "Ox0HAULT":
        print("[x] Income Tax service hault now.....")
        #process_name = 'selenium_test.exe'
        try:
            window_title="incometax"
            # subprocess.run(["start","cmd","/k",f"taskkill /F /PID {process_name}"],shell=True,check=True)
            #subprocess.run(["taskkill", "/F", "/IM", process_name], check=True)
            #print(f"Killed the process '{process_name}'.")
            # Use PowerShell to close the terminal window by title
            #subprocess.run("powershell.exe")
            powershell_script = f"Get-Process | Where-Object {{ $.MainWindowTitle -eq '{window_title}' }} | ForEach-Object {{ $.CloseMainWindow() }}"
            subprocess.run(["powershell.exe", "-Command", powershell_script], check=True)
            # 
            print(f"Closed terminal window with title: {window_title}")


        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        

    elif body.decode("utf-8") == "Ox1HAULT":
        try:
            
            window_title="gst"
            # subprocess.run(["start","cmd","/k",f"taskkill /F /PID {process_name}"],shell=True,check=True)
            #subprocess.run(["taskkill", "/F", "/IM", process_name], check=True)
            #print(f"Killed the process '{process_name}'.")
            # Use PowerShell to close the terminal window by title
            #subprocess.run("powershell.exe")
            powershell_script = f"Get-Process | Where-Object {{ $.MainWindowTitle -eq '{window_title}' }} | ForEach-Object {{ $.CloseMainWindow() }}"
            subprocess.run(["powershell.exe", "-Command", powershell_script], check=True)
            print(f"Closed terminal window with title: {window_title}")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Not any code given")
    method_frame,header_frame,body=ch.basic_get(queue='user1')
    if(method_frame):
        print(f'nextmessage {body}')
    else:
        print('no more messages')
            
    # print(f" [x] Received {body}")

def run_client():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('193.203.160.234'))
    channel = connection.channel()

    # Declare the same queue as the server
    channel.queue_declare(queue='user1')

    # Set up the callback function to handle incoming messages
    channel.basic_consume(queue='user1', on_message_callback=callback, auto_ack=True)
    channel.basic_qos(prefetch_count=1)

    print(' [*] Waiting for messages. To exit, press Ctrl+C')
    channel.start_consuming()

run_client()