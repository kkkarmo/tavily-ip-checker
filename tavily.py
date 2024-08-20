import re
import requests
import time
from datetime import datetime
import schedule
import json
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
# Tavily AI API key - replace with your actual key
# Flag to use mock responses instead of real API calls
#USE_MOCK_RESPONSES = True
USE_MOCK_RESPONSES = False

def read_vt_results(file_path):
    print(f"Attempting to read file: {file_path}")
    flagged_ips = []
    error_ips = []
    with open(file_path, 'r') as file:
        for line in file:
            print(f"Processing line: {line.strip()}")
            match = re.match(r"IP: (\d+\.\d+\.\d+\.\d+), (?:Malicious: (\d+), Suspicious: (\d+)|Error: (.+))", line)
            if match:
                ip, malicious, suspicious, error = match.groups()
                if error:
                    error_ips.append((ip, error))
                elif int(malicious) > 0 or int(suspicious) > 0:
                    flagged_ips.append((ip, int(malicious), int(suspicious)))
    print(f"Flagged IPs: {flagged_ips}")
    print(f"Error IPs: {error_ips}")
    return flagged_ips, error_ips

def mock_tavily_search(query):
    # Simulate API response
    mock_response = {
        "answer": f"This is a mock answer for the query: {query}",
        "results": [
            {
                "title": "Mock Result 1",
                "content": "This is the content of mock result 1..."
            },
            {
                "title": "Mock Result 2",
                "content": "This is the content of mock result 2..."
            },
            {
                "title": "Mock Result 3",
                "content": "This is the content of mock result 3..."
            }
        ]
    }
    return mock_response

def tavily_search(query):
    if USE_MOCK_RESPONSES:
        return mock_tavily_search(query)

    url = "https://api.tavily.com/search"
    headers = {
        "content-type": "application/json"
    }
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True
    }
    try:
        print(f"Sending request to Tavily API for query: {query}")
        print(f"API Key used: {TAVILY_API_KEY[:5]}...{TAVILY_API_KEY[-5:]}")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Content: {response.text[:500]}...")
        return response.json()
    except requests.RequestException as e:
        print(f"API Request Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error response: {e.response.text}")
        return {}

def process_ips():
    vt_result_file = "vt_results.txt"
    flagged_ips, error_ips = read_vt_results(vt_result_file)

    if not flagged_ips and not error_ips:
        print("No flagged or error IPs found.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"tavily_results_{timestamp}.txt"

    with open(output_file, 'w') as out_file:
        # Process flagged IPs
        for ip, malicious, suspicious in flagged_ips:
            print(f"Searching for information about IP: {ip} (Malicious: {malicious}, Suspicious: {suspicious})")
            out_file.write(f"IP: {ip} (Malicious: {malicious}, Suspicious: {suspicious})\n\n")

            queries = [
                f"Why is IP {ip} flagged as malicious or suspicious?",
                f"What can be found about IP {ip} in terms of cybersecurity aspects?"
            ]

            for query in queries:
                result = tavily_search(query)
                out_file.write(f"Query: {query}\n")
                if "answer" in result:
                    out_file.write(f"Answer: {result['answer']}\n\n")
                else:
                    out_file.write("No direct answer found.\n\n")

                out_file.write("Top Results:\n")
                for item in result.get("results", [])[:3]:
                    out_file.write(f"- {item['title']}\n")
                    out_file.write(f"  {item['content'][:200]}...\n\n")

            out_file.write("-" * 50 + "\n\n")
            if not USE_MOCK_RESPONSES:
                time.sleep(5)  # Add a 5-second delay between IP searches

        # Write summary of error IPs
        if error_ips:
            out_file.write("IPs with Errors:\n")
            for ip, error in error_ips:
                out_file.write(f"IP: {ip}, Error: {error}\n")
            out_file.write("\n" + "-" * 50 + "\n\n")

        # Write summary of all flagged IPs
        out_file.write("Summary of Flagged IPs:\n")
        for ip, malicious, suspicious in flagged_ips:
            out_file.write(f"IP: {ip}, Malicious: {malicious}, Suspicious: {suspicious}\n")

    print(f"Results saved to {output_file}")

def run_monday_midnight():
    if datetime.now().weekday() == 0 and datetime.now().hour == 0 and datetime.now().minute == 0:
        print("Running scheduled task on Monday at midnight")
        process_ips()
    else:
        print("Not Monday midnight. Skipping.")

if __name__ == "__main__":
    if USE_MOCK_RESPONSES:
        print("Running with mock responses")
        process_ips()
    else:
        schedule.every().day.at("00:00").do(run_monday_midnight)
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
