import requests

BASE_URL = "http://127.0.0.1:8000"  # ✅ FastAPI running locally

def test_process_dispute():
    url = f"{BASE_URL}/process_dispute/"  # ✅ Local FastAPI endpoint
    request_data = {
        "user_id": 4,
        "dispute": "My credit card was charged $89.99 for a subscription I canceled last month. I have the email confirmation of cancellation dated May 15th."
    }
    
    try:
        # Send a POST request to FastAPI
        response = requests.post(url, json=request_data)

        # ✅ Print response details
        print("\nPOST /process_dispute Response Status Code:", response.status_code)
        
        if response.status_code == 200:
            print("Response JSON:", response.json())  # ✅ Print the response for debugging
        else:
            print("Error Details:", response.text)
    
    except Exception as e:
        print("Error testing /process_dispute endpoint:", str(e))

if __name__ == "__main__":
    print("\nTesting FastAPI on localhost...")
    test_process_dispute()
