from django.shortcuts import render
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
import numpy as np
from .models import Product
from.serializers import ProductSerializer,RegisterSerializer,LOginxSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
class PredictView(APIView):
    def post(self, request):
        print(request.data)
        # Get the input data list from the request
        input_data = request.data.get('input_data', [])

        # Validate the input data
        if len(input_data) != 30:
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            model = load_model('can/cancer.h5')
            nparray=np.asarray(input_data)
            reshape=nparray.reshape(1,-1)
            standarddata=StandardScaler().fit_transform(reshape)
            z=model.predict(standarddata)

            g=np.argmax(z)
            if g==1: 
                return Response({'result': 'Malignant'}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'Benign'}, status=status.HTTP_200_OK)
class Productviewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
class Register(APIView):
    def post(self, request):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Logindata(APIView):
    def post(self, request):
        serializer = LOginxSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
            username=serializer.data['username'], 
            password=serializer.validated_data.get('password'))
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Print the model summary

# Create your views here.
