# Create your views here.
from django.http.response import HttpResponse
from rest_framework import viewsets
from movie.models import BasedOnId, BasedOnTitle
from movie.myserializer import BasedOnIdSerializer, BasedOnTitleSerializer
from movie import RecSysDJ
from rest_framework.response import Response

class BasedOnIdViewSet(viewsets.ModelViewSet):
    queryset = BasedOnId.objects.order_by("-id")
    serializer_class = BasedOnIdSerializer
    def create(self, request, *args, **kwargs):
        viewsets.ModelViewSet.create(self, request, *args, **kwargs)

        ob = BasedOnId.objects.latest("id")
        
        df = RecSysDJ.read_df()  
        movie_matrix = RecSysDJ.read_movie_matrix()      
        
        curated = RecSysDJ.get_curated(df)
        sim_user_top = RecSysDJ.get_sim_user_top_rated(df, movie_matrix, ob.user_id)
        
        return Response({"status": "Success", "curated": curated.to_json(), "sim_user_top": sim_user_top.to_json()})  # Your override
        

class BasedOnTitleViewSet(viewsets.ModelViewSet):
    queryset = BasedOnTitle.objects.order_by("-id")
    serializer_class = BasedOnTitleSerializer
    def create(self, request, *args, **kwargs):
        viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        ob = BasedOnTitle.objects.latest("id")
        
        df = RecSysDJ.read_df()  
        movie_matrix = RecSysDJ.read_movie_matrix()      
        similar = RecSysDJ.get_sim(df, movie_matrix, ob.title)        
        return Response({"status": "Success", "similar": similar.to_json()})  # Your override
        
        
        
