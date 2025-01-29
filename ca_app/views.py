from django.shortcuts import render
from rest_framework import viewsets
from django.core import serializers
from django.db import connection
from django.db import connections, DatabaseError
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.core.files.storage import FileSystemStorage
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import os
import base64
import datetime
import os.path
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated


def gstNoticeOrder(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT notice_download_gst_notice.id, notice_download_gst_clients.id AS 'client_id', notice_download_gst_clients.party_name, notice_download_gst_notice.notice_name, notice_download_gst_notice.issue_date, notice_download_gst_notice.issue_by, notice_download_gst_notice.status FROM notice_download_gst_notice INNER JOIN notice_download_gst_clients ON notice_download_gst_notice.client_id = notice_download_gst_clients.id")
            row = cursor.fetchall()
            
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, r)) for r in row]
        data = json.dumps(result,  default=str)
        return HttpResponse(data, content_type='application/json')

@api_view(['POST'])
def user_auth(request):
    data = request.data
    email = data['email']
    password = data['password']
    with connections['ca_cus'].cursor() as cursor:
        cursor.execute(" SELECT id, username, base_url FROM user WHERE email =%s AND password = %s ", [email, password])
        row = cursor.fetchone()
        print('user auth - ',row)
        
        if row != None:
            columns = [col[0] for col in cursor.description]
            result = dict(zip(columns, row)) 
            return JsonResponse({'success':True, 'message':'User is authenticated.',  'data': result})
        cursor.close()
        cursor.db.close()
    return JsonResponse({'success':False, 'message':'User\'s email or password is incorrect.',  })


@require_http_methods(["GET"])
def gst_sor_notice(request):
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT notice_download_gst_other_notice.id, notice_download_gst_clients.id AS 'client_id', notice_download_gst_clients.party_name, notice_download_gst_other_notice.notice_name, notice_download_gst_other_notice.issue_date, notice_download_gst_other_notice.due_date, notice_download_gst_other_notice.status FROM `notice_download_gst_other_notice` INNER JOIN notice_download_gst_clients ON notice_download_gst_other_notice.client_id = notice_download_gst_clients.id")
            row = cursor.fetchall()
            
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, r)) for r in row]
        # data = json.dumps(result,  default=str)
        # return HttpResponse(data, content_type='application/json')
        return JsonResponse({"success": True, "message":"fetched some list", "data": result})
    except Exception as e:
        return JsonResponse({"success": False, "message":"list could not be found.",})
    

  
@api_view(['POST', 'PATCH', 'DELETE'])
def client_info(request):
    if request.method == 'POST':
        try:
            data = request.data
            party_name = data['party_name']
            username = data['username']
            password = data['password']
            sectionType = data['type']
            with connections['notice'].cursor() as cursor:
                if sectionType == 'gst':
                    cursor.execute("INSERT INTO notice_download_gst_clients (party_name, username, password, flag) VALUES(%s,%s,%s,'-1')",[party_name,username,password])
                else:
                    cursor.execute("INSERT INTO notice_download_it_clients (party_name, username, password, flag) VALUES(%s,%s,%s,'-1')",[party_name,username,password])
                cursor.db.commit()
                cursor.close()
                cursor.db.close()
            return JsonResponse({'success': True, 'message': 'New record has been added successfully.'})
            # return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'success': False, "error": str(e)})
        
    if request.method == 'PATCH':
        try:
            data = request.data
            client_id = data['id']
            party_name = data['party_name']
            username = data['username']
            password = data['password']
            sectionType = data['type']
            with connections['notice'].cursor() as cursor:
                if sectionType == 'gst':
                    cursor.execute("UPDATE notice_download_gst_clients SET party_name = %s, username = %s, password = %s WHERE id = %s ",[party_name,username,password,client_id])
                else:
                    cursor.execute("UPDATE notice_download_it_clients SET party_name = %s, username = %s, password = %s WHERE id = %s ",[party_name,username,password,client_id])
                if cursor.rowcount > 0:
                    success = True
                    message =  "A record has been updated successfully."
                else:
                    success = False
                    message = "A record couldn\'t updated."
                cursor.db.commit()
                cursor.close()
                cursor.db.close()
            return JsonResponse({'success': success , 'message' : message })
            # return JsonResponse(data)
        except DatabaseError as de:
            return JsonResponse({'success':False, "error": str(de)})
        except Exception as e:
            return JsonResponse({'success': False,"error": str(e)})
    if request.method == 'DELETE':
        try:
            data = request.data
            client_id = data['id']
            sectionType = data['type']
            
            with connections['notice'].cursor() as cursor:
                try:
                    if sectionType == 'gst':
                        cursor.execute("DELETE FROM notice_download_gst_clients WHERE id = %s ",[client_id])
                    else:
                        cursor.execute("DELETE FROM notice_download_it_clients WHERE id = %s ",[client_id])
                    cursor.db.commit()
                    cursor.close()
                    cursor.db.close()
                    
                except Exception as e:
                    cursor.close()
                    cursor.db.close()
                    return JsonResponse({'success': False,"error": str(e)})
                
                # status_message = cursor.rownumber
            
            return JsonResponse({'success': True, 'message': 'A record has been deleted successfully.',})
            # return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'success': False,"error": str(e)})

@api_view(['POST'])
def upload_file(request):
    data_file = request.FILES
    excel_file = data_file['file']
    sectionType = request.data['type']
    print('type = ', sectionType)
    fs = FileSystemStorage()
    fileName = fs.save('upload/'+excel_file.name, excel_file)
    file_path = fs.url(fileName)
    
    df = pd.read_excel(fs.path(fileName))
    rows = []
    for _,row in df.iterrows():
        # print(row['party_name'],' ',row['username'],' ',row['password'])
        # tp = tuple(row)
        party_name = row['party_name']
        username : str = row['username']
        username_bytes : bytes = base64.b64encode(username.encode())
        enc_username = username_bytes.decode()
        password : str = row['password']
        password_bytes : bytes = base64.b64encode(password.encode())
        enc_password = password_bytes.decode()

        rows.append(tuple([party_name,enc_username,enc_password]))
        # print(tp)
    fs.delete(fileName)
    print(rows)
    with connections['notice'].cursor() as cursor:
        try:
            if sectionType == 'gst':
                cursor.executemany("INSERT INTO notice_download_gst_clients (party_name, username, password, flag) VALUES(%s,%s,%s,'-1')", rows)
            else:
                cursor.executemany("INSERT INTO notice_download_it_clients (party_name, username, password, flag) VALUES(%s,%s,%s,'-1')", rows)
            cursor.db.commit()
            cursor.close()
            cursor.db.close()
            return JsonResponse({'success': True ,'message':'file has been saved', 'result':'Records are added successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}) 
    
@api_view(['POST'])
def view_file(request):
    s3_client = boto3.resource(service_name='s3',
    region_name='ap-south-1',
    aws_access_key_id='AKIAX2MHZPD6X6YQ2C5B',
    aws_secret_access_key='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'
)
    fs = FileSystemStorage()
    data = request.data
    file_name : str = data['fileName']
    file_path : str = data['filePath']
    
    # s3_client.meta.client.download_file('demo-patronaid', 'GST/APPEAL/Orders/GST APL-02.pdf', 'GST APL-02.pdf')
    try:
        if not os.path.exists(settings.MEDIA_ROOT+"/view/"):
            os.mkdir(settings.MEDIA_ROOT+"view/")
        path = settings.MEDIA_ROOT+"view/"
        s3_client.meta.client.download_file('demo-patronaid', file_path, path+file_name)
        
        return JsonResponse({'success':True,'message':'file found.','file_url': f'http://ca.patronaidtechnologies.site/api/downloadFile/?fileName={file_name}' })
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return JsonResponse({'success':False,'error': e.response['Error']})
        else:
            return JsonResponse({'success':False,'error': e.response['Error']})


@api_view(['GET'])
def download_file(request):
    file_name = request.GET.get('fileName')
    file_path = settings.MEDIA_ROOT+"/view/"+file_name
    with open(file_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f' inline; filename={file_name}'
   # return render(request, 'pdf.html', {'pdf_file':file_path})
    return response

@api_view(['PATCH'])
def notice_status(request):
    data = request.data
    notice_id = data['id']
    type_id  = data['typeId']
    status = data['status']
    with connections['notice'].cursor() as cursor:
        try:
            if type_id == '1':
                print('notice id',notice_id)
                cursor.execute("UPDATE notice_download_it_notice SET status = %s WHERE id = %s ",[status, notice_id] )
                
            elif type_id == '2':
                cursor.execute("UPDATE scrutiny_of_returns SET status = %s WHERE id = %s ",[status, notice_id] )
            elif type_id == '3':
                cursor.execute("UPDATE determination_of_tax SET status = %s WHERE id = %s ",[status, notice_id] )
            elif type_id == '4':
                cursor.execute("UPDATE appeal SET status = %s WHERE id = %s ",[status, notice_id] )
            elif type_id == '5':
                cursor.execute("UPDATE notice_download_gst_notice SET status = %s WHERE id = %s ",[status, notice_id] )
            else:
                print('else notice id',notice_id)

            cursor.db.commit()
            cursor.close()
            cursor.db.close()
            return JsonResponse({'success':True,'message':'Status has been changed.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success':False,'error':str(e)})


@api_view(['GET'])
def notice(request):
    section_type : str = request.GET.get('sectionType')
    
    
    with connections['notice'].cursor() as cursor:
        
        match section_type:
            case 'notice&order':
                cursor.execute(" SELECT ( ROW_NUMBER() OVER ( ORDER BY notice_download_gst_notice.id ) )AS 'uid' , notice_download_gst_notice.id, notice_download_gst_clients.party_name, notice_download_gst_notice.client_id, notice_download_gst_notice.notice_name , notice_download_gst_notice.issue_date , notice_download_gst_notice.issue_by ,notice_download_gst_notice.status, notice_download_gst_notice.attachment FROM notice_download_gst_notice INNER JOIN notice_download_gst_clients ON notice_download_gst_notice.client_id = notice_download_gst_clients.id WHERE notice_download_gst_notice.status IN ('Not Started', 'Started') "  )
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'sor':
                cursor.execute(" SELECT ( ROW_NUMBER() OVER ( ORDER BY scrutiny_of_returns.id ) )AS 'uid' , scrutiny_of_returns.id, notice_download_gst_clients.party_name, scrutiny_of_returns.client_id, scrutiny_of_returns.category, scrutiny_of_returns.type, scrutiny_of_returns.reference_or_order_num, scrutiny_of_returns.issue_date, scrutiny_of_returns.due_date, scrutiny_of_returns.order_date, scrutiny_of_returns.section, scrutiny_of_returns.personal_hearing, scrutiny_of_returns.status, scrutiny_of_returns.attachment FROM `scrutiny_of_returns` INNER JOIN notice_download_gst_clients ON scrutiny_of_returns.client_id = notice_download_gst_clients.id WHERE scrutiny_of_returns.status IN ('Not Started', 'Started') "  )
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'dot':
                cursor.execute(" SELECT ( ROW_NUMBER() OVER ( ORDER BY determination_of_tax.id ) )AS 'uid' , determination_of_tax.id, notice_download_gst_clients.party_name, determination_of_tax.client_id, determination_of_tax.category, determination_of_tax.type, determination_of_tax.reference_or_order_num, determination_of_tax.issue_date, determination_of_tax.due_date, determination_of_tax.order_date, determination_of_tax.section, determination_of_tax.personal_hearing, determination_of_tax.status, determination_of_tax.attachment FROM determination_of_tax INNER JOIN notice_download_gst_clients ON determination_of_tax.client_id = notice_download_gst_clients.id WHERE determination_of_tax.status IN ('Not Started', 'Started') " )
                row = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'appeal':
                cursor.execute(" SELECT ( ROW_NUMBER() OVER ( ORDER BY appeal.id ) )AS 'uid' , appeal.id, notice_download_gst_clients.party_name, appeal.client_id, appeal.category, appeal.order_num, appeal.order_date, appeal.status, appeal.attachment FROM appeal INNER JOIN notice_download_gst_clients ON appeal.client_id = notice_download_gst_clients.id WHERE appeal.status IN ('Not Started', 'Started') " )
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'it':
                cursor.execute(" SELECT ( ROW_NUMBER() OVER ( ORDER BY notice_download_it_notice.id ) )AS 'uid' , notice_download_it_notice.id, notice_download_it_clients.party_name, notice_download_it_notice.client_id, notice_download_it_notice.notice_name , notice_download_it_notice.issue_date , notice_download_it_notice.assessment_year ,notice_download_it_notice.status, notice_download_it_notice.attachment FROM notice_download_it_notice INNER JOIN notice_download_it_clients ON notice_download_it_notice.client_id = notice_download_it_clients.id WHERE notice_download_it_notice.status IN ('Not Started', 'Started') "  )
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case _:
                return JsonResponse({'success': False})


@api_view(['GET'])
def history(request):
    section_type : str = request.GET.get('sectionType')
    client_id = request.GET.get('id')
    
    with connections['notice'].cursor() as cursor:
        
        match section_type:
            case 'notice&order':
                cursor.execute("SELECT id, client_id, notice_name, issue_date, issue_by, status FROM notice_download_gst_notice WHERE client_id = %s and status = 'Completed' ", (client_id))
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'sor':
                cursor.execute("SELECT id, client_id, category, type, reference_or_order_num, issue_date, due_date, order_date, section, personal_hearing , status, attachment FROM scrutiny_of_returns WHERE client_id = %s and status = 'Completed' ", (client_id))
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'dot':
                cursor.execute("SELECT id, client_id, category, type, reference_or_order_num, issue_date, due_date, order_date, section, personal_hearing , status, attachment FROM determination_of_tax WHERE client_id = %s and status = 'Completed' ", (client_id))
                row = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'appeal':
                cursor.execute("SELECT id, client_id, category, order_num, order_date, status, attachment FROM appeal WHERE client_id = %s and status = 'Completed' ", (client_id))
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case 'it':
                cursor.execute("SELECT id, client_id, notice_name, issue_date, assessment_year, status, attachment FROM notice_download_it_notice WHERE client_id = %s and status = 'Completed' ", (client_id))
                row = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, r)) for r in row]
                print( len(result) )
                cursor.close()
                cursor.db.close()
                if len(result) > 0:
                    return JsonResponse({'success':True, 'message':'records are found.', 'data': result})
                else :
                    return JsonResponse({'success':False, 'message':'records are not available.' })
            case _:
                return JsonResponse({'success': False})
    
@api_view(['POST'])
def clients(request):
    section_type = request.data['sectionType']
    
    with connections['notice'].cursor() as cursor:
        if section_type == 'gst':
            cursor.execute("SELECT ( ROW_NUMBER() OVER ( ORDER BY id ) )AS 'uid' , id, party_name, username, password, created_at FROM notice_download_gst_clients ")
        else:
            cursor.execute("SELECT ( ROW_NUMBER() OVER ( ORDER BY id ) )AS 'uid' ,id, party_name, username, password, created_at FROM notice_download_it_clients ")
        cursor.db.commit()
        row = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, r)) for r in row]
        cursor.close()
        cursor.db.close()
        if len(result) > 0:
            return JsonResponse({'success':True, 'message': 'records are found.', 'data': result})
        else:
            return JsonResponse({'success':False, 'message': 'records are not found.'})

@api_view(['POST'])
def reminder(request):
  SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file( settings.GOOGLE_OAUTH2_CLIENT_SECRET_JSON , SCOPES )
      flow.redirect_uri = "http://127.0.0.1:8080"
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")



class GoogleLogin(APIView):
    def get(self, request, *args, **kwargs):
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRET_JSON,
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=request.build_absolute_uri(reverse('google_callback'))
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        request.session['state'] = state
        return redirect(authorization_url)

class GoogleCallback(APIView):
    def get(self, request, *args, **kwargs):
        state = request.session['state']
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRET_JSON,
            scopes=['https://www.googleapis.com/auth/calendar'],
            state=state,
            redirect_uri=request.build_absolute_uri(reverse('google_callback'))
        )
        flow.fetch_token(authorization_response=request.get_full_path())
        credentials = flow.credentials
        request.session['credentials'] = credentials_to_dict(credentials)
        return Response({"message": "Authentication successful"})
    

class AddEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        creds_data = request.session.get('credentials')
        creds = Credentials(**creds_data)
        service = build('calendar', 'v3', credentials=creds)

        event = request.data.get('event')  # Assuming event details are passed as JSON
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return Response({"message": "Event created", "eventLink": created_event.get('htmlLink')})

@api_view(['GET'])
def get_credentials(request):
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds = None
    if(os.path.exists(r'token.json')):
        creds = Credentials.from_authorized_user_file(r'token.json')
    
    if not creds or creds.valid:
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(settings.GOOGLE_OAUTH2_CLIENT_SECRET_JSON, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
            # creds = flow.run_console()
            

        with open(r'token.json', 'w') as token:
            token.write(creds.to_json())
    #return creds
    service = build("calendar","v3", credentials= creds)
    create_event_with_reminders(service= service)


def create_event_with_reminders(service):
    try:
        event = {
            "summary" : "Meeting with reminders",
            "location" : "None",
            "start" : {
                "datetime" : "2024-05-07T07:00:00+05:30",
                "timezone": "Asia/Kolkata",
            },
            "end": {
                "datetime" : "2024-05-07T18:00:00+05:30",
                "timezone": "Asia/Kolkata",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {
                    "method": "popup",
                    "minutes": 30
                },
                {
                    "method": "email",
                    "minutes": 60
                },
            ]
            }
        }
        
        created_event = service.events().insert(calendarId="primary", body = event).execute()
        print(f"Event is created successfully... {created_event.get('htmlLink')}")
        print(f"Event id is generated  {created_event['id'] }")
    except Exception as e:
        print(f"An error occurred - {e}")