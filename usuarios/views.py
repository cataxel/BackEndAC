from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

def test_db_connection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        return HttpResponse(f"Database connection successful: {row}")
    except Exception as e:
        return HttpResponse(f"Database connection failed: {e}")