import urllib.request
import json
import sys

# Change this to False to test production
TEST_LOCAL = True

if TEST_LOCAL:
    url = "http://127.0.0.1:10000/chat/"
    print("Testing LOCAL backend on port 10000...")
else:
    url = "https://echomind-backend-w74f.onrender.com/chat/"
    print("Testing PRODUCTION backend on Render...")

data = json.dumps({"message": "hello"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        body = response.read().decode('utf-8')
        print(f"Response Body: {body}")
        
        # Verify JSON
        try:
            json_resp = json.loads(body)
            if "response" in json_resp:
                print("SUCCESS: Received valid chat response.")
            else:
                print("WARNING: Response JSON missing 'response' field.")
        except:
            print("ERROR: Response is not valid JSON.")
            
except urllib.error.HTTPError as e:
    print(f"Status Code: {e.code}")
    print(f"Response Body: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Request failed: {e}")
    if TEST_LOCAL:
        print("TIP: Make sure the local server is running (python main.py)")
