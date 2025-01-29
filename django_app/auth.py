from django.db import connections
from django.http import  JsonResponse
from rest_framework.decorators import api_view

@api_view(['POST'])
def user_auth(request):
    data = request.data
    email = data['email']
    password = data['password']
    with connections['ca_cus'].cursor() as cursor:
        cursor.execute(" SELECT id, first_name, username, base_url FROM user WHERE email =%s AND password = %s ", [email, password])
        row = cursor.fetchone()
        print('user auth - ',row)
        
        if row != None:
            columns = [col[0] for col in cursor.description]
            result = dict(zip(columns, row)) 
            return JsonResponse({'success':True, 'message':'User is authenticated.',  'data': result})
        cursor.close()
        cursor.db.close()
    return JsonResponse({'success':False, 'message':'User\'s email or password is incorrect.',  })