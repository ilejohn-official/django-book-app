from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializer import BookSerializer

@api_view(['GET'])
def get_books(request):
  books = Book.objects.all()
  serializer = BookSerializer(books, many=True)

  return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_book(request):
  data = request.data
  serializer = BookSerializer(data=data)
  if not data:
    return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)
  if not serializer.is_valid():
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  serializer.save()
  return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def book_details(request, pk):
  try:
    book = Book.objects.get(pk=pk)
  except Book.DoesNotExist:
    return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'PUT':
    data = request.data
    serializer = BookSerializer(book, data=data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  elif request.method == 'DELETE':
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  elif request.method == 'GET':
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)