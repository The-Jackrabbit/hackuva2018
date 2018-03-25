from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from .forms import SearchForm
from .models import Season, Tournament, Set, Game, User, PowerRank, PowerRankToUsers, TournamentToUsers, BadgesToUsers, Badge, FileUpload

from .serializers import UserSerializer, SeasonSerializer, TournamentSerializer, SetSerializer, GameSerializer, FileUploadSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils import timezone
from django.db.models import Q
from django.core.files import File  # you need this somewhere
import urllib
import os
import random

from rest_framework.parsers import FileUploadParser

def upload_image(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES.get('file'))
        return HttpResponse("Successful")

    return HttpResponse("Failed")

class FileUploadViewSet(viewsets.ModelViewSet):
    
	queryset = FileUpload.objects.all()
	serializer_class = FileUploadSerializer
	parser_classes = (FileUploadParser, )

	def perform_create(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'status': '201 - Created', 'result': serializer.data}, status=status.HTTP_201_CREATED)
		return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		
''' API ENDPOINTS '''
class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	renderer_classes = (JSONRenderer, )
	queryset = User.objects.all()
	serializer_class = UserSerializer
	model = User
	
	def delete(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to delete an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
				result.delete()
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'User with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			except IntegrityError:
				return Response({'status': '400 - Bad Request', 'result': 'User is a foreign key to other models and thus cannot be deleted'}, status=status.HTTP_409_CONFLICT)
			return Response({'status': '204 - No Content', 'response': "Successfully deleted user"})
		
	def get(self, request, format=None, pk=None):
		is_many = True
		if pk is None:
			result = self.model.objects.all()
		else:
			try:
				result = self.model.objects.get(pk=pk)
				is_many = False
			except self.model.DoesNotExist:
				return Response({'status': '404', 'result': 'User with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
		
		serializer = self.serializer_class(result, many=is_many)
		return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
	
	def post(self, request, format=None, pk=None):
		if pk is None:
			serializer = self.serializer_class(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': '201 - Created', 'result': serializer.data}, status=status.HTTP_201_CREATED)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'status': '400 - Bad Request', 'result': 'Cannot POST data to an already created id'}, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to update an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'User with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			
			serializer = self.serializer_class(result, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		

class SeasonViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows seasons to be viewed or edited.
	"""
	renderer_classes = (JSONRenderer, )
	queryset = Season.objects.all()
	serializer_class = SeasonSerializer

	model = Season
	
	def delete(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to delete an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
				result.delete()
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Season with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			except IntegrityError:
				return Response({'status': '400 - Bad Request', 'result': 'Season is a foreign key to other models and thus cannot be deleted'}, status=status.HTTP_409_CONFLICT)
			return Response({'status': '204 - No Content', 'response': "Successfully deleted season"})
		
	def get(self, request, format=None, pk=None):
		is_many = True
		if pk is None:
			result = self.model.objects.all()
		else:
			try:
				result = self.model.objects.get(pk=pk)
				is_many = False
			except self.model.DoesNotExist:
				return Response({'status': '404', 'result': 'Season with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
		
		serializer = self.serializer_class(result, many=is_many)
		return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
	
	def post(self, request, format=None, pk=None):
		if pk is None:
			serializer = self.serializer_class(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': '201 - Created', 'result': serializer.data}, status=status.HTTP_201_CREATED)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'status': '400 - Bad Request', 'result': 'Cannot POST data to an already created id'}, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to update an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Season with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			
			serializer = self.serializer_class(result, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
	

class TournamentViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows tournaments to be viewed or edited.
	"""
	renderer_classes = (JSONRenderer, )
	queryset = Tournament.objects.all()
	# cannot abstract serializer_class because it requires a request to be instantiated, and
	# the request isn't passed until the function executes
	serializer_class = TournamentSerializer

	model = Tournament
	
	def delete(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to delete an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
				result.delete()
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Tournament with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			except IntegrityError:
				return Response({'status': '400 - Bad Request', 'result': 'Tournament is a foreign key to other models and thus cannot be deleted'}, status=status.HTTP_409_CONFLICT)
			return Response({'status': '204 - No Content', 'response': "Successfully deleted tournament"})
		
	def get(self, request, format=None, pk=None):
		is_many = True
		if pk is None:
			result = self.model.objects.all()
		else:
			try:
				result = self.model.objects.get(pk=pk)
				is_many = False
			except self.model.DoesNotExist:
				return Response({'status': '404', 'result': 'Tournament with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
		serializer_context = {
			'request': request,
		}
		serializer = TournamentSerializer(result, context=serializer_context, many=is_many)
		return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
	
	def post(self, request, format=None, pk=None):
		if pk is None:
			serializer_context = {
				'request': request,
			}
			serializer = TournamentSerializer(data=request.data, context=serializer_context)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': '201 - Created', 'result': serializer.data}, status=status.HTTP_201_CREATED)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'status': '400 - Bad Request', 'result': 'Cannot POST data to an already created id'}, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to update an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Tournament with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			
			serializer_context = {
				'request': request,
			}
			serializer = TournamentSerializer(result, data=request.data, context=serializer_context)

			if serializer.is_valid():
				serializer.save()
				return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SetViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows sets to be viewed or edited.
	"""
	renderer_classes = (JSONRenderer, )
	queryset = Set.objects.all()
	serializer_class = SetSerializer

	model = Set
	
	def delete(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to delete an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
				result.delete()
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Set with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			except IntegrityError:
				return Response({'status': '400 - Bad Request', 'result': 'Set is a foreign key to other models and thus cannot be deleted'}, status=status.HTTP_409_CONFLICT)
			return Response({'status': '204 - No Content', 'response': "Successfully deleted set"})
		
	def get(self, request, format=None, pk=None):
		is_many = True
		if pk is None:
			result = self.model.objects.all()
		else:
			try:
				result = self.model.objects.get(pk=pk)
				is_many = False
			except self.model.DoesNotExist:
				return Response({'status': '404 - Object Not Found', 'result': 'Set with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
		serializer_context = {
			'request': request,
		}
		serializer = SetSerializer(result, context=serializer_context, many=is_many)
		return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
	
	def post(self, request, format=None, pk=None):
		if pk is None:
			serializer_context = {
				'request': request,
			}
			serializer = SetSerializer(data=request.data, context=serializer_context)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': '201 - Created', 'result': serializer.data}, status=status.HTTP_201_CREATED)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'status': '400 - Bad Request', 'result': 'Cannot POST data to an already created id'}, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to update an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Set with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			
			serializer_context = {
				'request': request,
			}
			serializer = SetSerializer(result, data=request.data, context=serializer_context)

			if serializer.is_valid():
				serializer.save()
				return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GameViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows games to be viewed or edited.
	"""
	renderer_classes = (JSONRenderer, )
	queryset = Game.objects.all()
	serializer_class = GameSerializer

	model = Game
	
	def delete(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to delete an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
				result.delete()
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Game with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			except IntegrityError:
				return Response({'status': '400 - Bad Request', 'result': 'Game is a foreign key to other models and thus cannot be deleted'}, status=status.HTTP_409_CONFLICT)
			return Response({'status': '204 - No Content', 'response': "Successfully deleted game"})
		
	def get(self, request, format=None, pk=None):
		is_many = True
		if pk is None:
			result = self.model.objects.all()
		else:
			try:
				result = self.model.objects.get(pk=pk)
				is_many = False
			except self.model.DoesNotExist:
				return Response({'status': '404 - Object Not Found', 'result': 'Game with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
		serializer_context = {
			'request': request,
		}
		serializer = GameSerializer(result, context=serializer_context, many=is_many)
		return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
	
	def post(self, request, format=None, pk=None):
		if pk is None:
			serializer_context = {
				'request': request,
			}
			serializer = GameSerializer(data=request.data, context=serializer_context)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': '201 - Created', 'result': serializer.data}, status=status.HTTP_201_CREATED)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'status': '400 - Bad Request', 'result': 'Cannot POST data to an already created id'}, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, format=None, pk=None):
		if pk is None:
			return Response({'status': '400 - Bad Request', 'result': 'Please specify ID to update an entry'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				result = self.model.objects.get(pk=pk)
			except self.model.DoesNotExist:
				return Response({'status': '404 - Not Found', 'result': 'Game with given id does not exist'}, status=status.HTTP_404_NOT_FOUND)
			
			serializer_context = {
				'request': request,
			}
			serializer = GameSerializer(result, data=request.data, context=serializer_context)

			if serializer.is_valid():
				serializer.save()
				return Response({'status': '200 - OK', 'result': serializer.data}, status=status.HTTP_200_OK)
			return Response({'status': '400 - Bad Request', 'missing data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		
