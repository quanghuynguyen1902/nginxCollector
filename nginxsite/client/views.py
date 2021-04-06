from module.client import montoring
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, schema


class Requests(APIView):
    permissions_classes = [AllowAny]
    def get(self, request):        
        app_id = '593a13e1'
        page = self.request.GET.get('page', None)
        if(page):
            data, counts = montoring.get_data(app_id, page) 
        else:
            data, counts = montoring.get_data(app_id) 
        return Response({'counts': counts, 'results': data})
    
    

@api_view(['GET'])
def filter(request):  
    app_id = '593a13e1'
    request_method = request.GET.get('method')
    user_id = request.GET.get('user_id', None)
    url = request.GET.get('url', None)
    page = request.GET.get('page', None)
    time_from = request.GET.get('time_from', None)
    if(page):
        page = int(page)
        data, counts =  montoring.filter_data(app_id, request_method, user_id, url, time_from, page)
    else:
        data, counts = montoring.filter_data(app_id, request_method, user_id, time_from, url)
        
    return Response({'counts': counts, 'results': data})


@api_view(['GET'])
def get_users(request):  
    app_id = '593a13e1'
    keys, users = montoring.get_users(app_id)
    return Response({'keys': keys, 'results': users})

@api_view(['GET'])
def request_method_analytic(request):  
    app_id = '593a13e1'
    user_id = request.GET.get('user_id')
    total, methods = montoring.request_of_user(app_id, user_id)
    return Response({'total': total, 'methods': methods})

@api_view(['GET'])
def user_detail(request):  
    app_id = '593a13e1'
    user_id = request.GET.get('user_id')
    page = request.GET.get('page')
    counts, data = montoring.get_user_detail(app_id, user_id, page)
    return Response({'counts': counts, 'results': data})