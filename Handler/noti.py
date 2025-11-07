import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from pywebpush import webpush, WebPushException
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials, messaging
from time import *
import threading
from itertools import permutations
from pathlib import Path
import threading
BASE_DIR = Path(__file__).resolve().parent.parent
# Initialize Firebase Admin SDK with your service account file
cred = credentials.Certificate(f"{BASE_DIR}/static/noti-6c9df-firebase-adminsdk-6ywx1-af85becce4.json")
firebase_admin.initialize_app(cred)
from .Extra import *

@csrf_exempt
def save_subscription(request):
    if request.method == 'POST':
        try:
                data = json.loads(request.body)
                print(data["cookie_id"])
                c = Cookie_Handler.objects.get(Cookie=data["cookie_id"])
                s = Visa_Info.objects.filter(id=c.User).update(FCM=data["fcm_token"])

            # Here you could save to your database or perform actions needed
                return JsonResponse({'status': 'Subscription saved!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
# utils.py or in views.py


def send_push_notification(id, title, body):
    # Construct the message
    print(id)
    st = Visa_Info.objects.get(id=id)
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=st.FCM,
    )
    # Send the message and catch any errors
    try:
        response = messaging.send(message)
        print(f'Successfully sent message: {response}')
    except firebase_admin.exceptions.FirebaseError as e:
        print(f'Error sending message:')

# Example usage
#device_token = "fR22XvE2QvKzDrC-C6X89s:APA91bGA4iMFJXb-3CNodyuk3tBkyFrMo5f6N6pY4dePZd1nxzC6_gB8kfEdv8Esn1scTl6Lj7DxRqH8XTogq8lXQteALLkGTKkXu4u1pafIOKyePFH-XCQ"  # Replace with actual device token
#send_push_notification(device_token, "GTA🤣", "you may want to fetch a new FCM token when a user logs out and another logs in. This approach depends on your app’s design.")


from django.shortcuts import HttpResponse
from django.db import connections, transaction
#from .models import (Check_Cash, Momo_Cash, Expensis_Cash, Schedule_Markers_Multi,
#                     Schedule_Employees_Multi, Guest, Guest_Log, Switch_Log)
from django.apps import apps

import threading
from django.db import transaction, connection
from django.apps import apps


def duplicate_data_thread():
    """Copy data from SQLite to PostgreSQL and reset ID sequence properly."""
    models_to_duplicate = apps.get_app_config('Handler').get_models()

    try:
        with transaction.atomic(using='default'):  # PostgreSQL Transaction
            for model in models_to_duplicate:
                records = model.objects.using('sqlite').all()
                print(f'Duplicating {records.count()} records from {model.__name__}')

                for record in records:
                    record.save(using='default')  # Keep the same ID in PostgreSQL

            # 🔹 Properly reset ID sequence so Django inserts work correctly
            with connection.cursor() as cursor:
                for model in models_to_duplicate:
                    table_name = model._meta.db_table
                    primary_key_column = model._meta.pk.column

                    # Get the highest existing ID in PostgreSQL
                    cursor.execute(f"SELECT COALESCE(MAX({primary_key_column}), 0) FROM {table_name};")
                    last_id = cursor.fetchone()[0]

                    # Update sequence to start from the correct last ID + 1
                    cursor.execute(f"""
                        SELECT setval(
                            pg_get_serial_sequence('{table_name}', '{primary_key_column}'),
                            {last_id} + 1,
                            false
                        );
                    """)

                    print(f"✅ Sequence reset for {table_name}, next ID: {last_id + 1}")

        print("✅ Data duplication completed successfully with correct ID sequence.")

    except Exception as e:
        print(f"❌ Error in duplication: {e}")

def duplicate_data():
    """Start data duplication in a separate thread."""
    thread = threading.Thread(target=duplicate_data_thread)
    thread.daemon = True  # Ensures the thread stops if Django restarts
    thread.start()

    return 11  # Keeps original return value

from django.db import connection
from django.apps import apps

from django.db import connection
from django.apps import apps

def fix_postgres_sequences():
    """Ensure PostgreSQL ID sequences are correctly updated for all models, skipping missing tables."""
    models_to_fix = apps.get_app_config('Handler').get_models()

    try:
        with connection.cursor() as cursor:
            # 🔹 Fetch all existing table names in PostgreSQL (case-sensitive)
            cursor.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public';
            """)
            existing_tables = {row[0] for row in cursor.fetchall()}  # Set of table names (case-sensitive)

            for model in models_to_fix:
                table_name = model._meta.db_table  # Get the Django model table name (case-sensitive)
                primary_key_column = model._meta.pk.column  # Get primary key column name

                # 🔹 Skip if table does not exist
                if table_name not in existing_tables:
                    print(f"⚠️ Skipping {table_name}: Table does not exist in PostgreSQL.")
                    continue

                try:
                    # 🔹 Get the highest existing ID
                    cursor.execute(f'SELECT COALESCE(MAX("{primary_key_column}"), 0) FROM "{table_name}";')
                    last_id = cursor.fetchone()[0]

                    # 🔹 Check if the sequence exists before trying to reset it
                    cursor.execute(f"""
                        SELECT pg_get_serial_sequence('"public"."{table_name}"', '{primary_key_column}');
                    """)
                    sequence_name = cursor.fetchone()[0]

                    if not sequence_name:
                        print(f"⚠️ Skipping {table_name}: No sequence found.")
                        continue

                    # 🔹 Reset the sequence to the correct next ID
                    cursor.execute(f"SELECT setval('{sequence_name}', {last_id} + 1, false);")

                    print(f"✅ Sequence fixed for {table_name}, next ID: {last_id + 1}")

                except Exception as e:
                    print(f"❌ Error fixing sequence for {table_name}: {e}")

        print("🎯 PostgreSQL sequences successfully updated!")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
