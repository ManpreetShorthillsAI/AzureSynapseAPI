from django.shortcuts import render
from django.http import JsonResponse
import pyodbc

# Define connection parameters
server = 'synapse-tranning-ondemand.sql.azuresynapse.net'
database = 'Synapse'
username = 'tester'
password = '5&Y*9!Q#P'
driver = '{ODBC Driver 17 for SQL Server}'

# Function to establish connection to Synapse
def get_db_connection():
    connect_var= pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    print (connect_var)
    return connect_var

def get_data(request):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        print(conn)
        cursor = conn.cursor()

        page_number = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        offset = (page_number - 1) * page_size

        cursor.execute('SELECT * FROM samNewTest ORDER BY PID OFFSET ? ROWS FETCH NEXT ? ROWS ONLY', (offset, page_size))
        rows = cursor.fetchall()

        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def filter_data(request):
    # Get the PropertyState parameter from the request's query parameters
    property_state = request.GET.get('PropertyState')
    
    if not property_state:
        return JsonResponse({'error': 'PropertyState parameter is required'}, status=400)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # cursor.execute('SELECT TOP 100* FROM samNewTest WHERE PropertyState = ?', (property_state,))
        page_number = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        offset = (page_number - 1) * page_size

        cursor.execute('SELECT * FROM samNewTest WHERE PropertyState = ? ORDER BY PID OFFSET ? ROWS FETCH NEXT ? ROWS ONLY', (property_state,offset, page_size))
        rows = cursor.fetchall()
        
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()