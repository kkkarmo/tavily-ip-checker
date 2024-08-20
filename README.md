# Tavily IP Checker

Tavily IP Checker is a Python-based tool that processes a list of IP addresses, checks them against the Tavily API for malicious or suspicious activity, and generates a detailed report. This tool is designed to help cybersecurity professionals and network administrators quickly identify potentially harmful IP addresses in their networks.

## Installation

### Prerequisites
- Docker
- Tavily API key

### Steps
1. Clone the repository:

git clone https://github.com/kkkarmo/tavily-ip-checker.git
cd tavily-ip-checker
text

2. Build the Docker image:

docker build -t tavily-ip-checker .
text

## Usage

1. Prepare your input file:
Create a file named `vt_results.txt` in the same directory as the Dockerfile. Each line should contain an IP address and its status in the following format:

IP: 192.168.1.1, Malicious: 0, Suspicious: 0
text

2. Run the Docker container:

docker run -e TAVILY_API_KEY=your_actual_api_key -v $(pwd):/app tavily-ip-checker
text
Replace `your_actual_api_key` with your Tavily API key.

3. Check the output:
The script will generate a file named `tavily_results_YYYYMMDD_HHMMSS.txt` in the same directory, containing the analysis results.

## Use Case Scenario

A network administrator wants to check a list of IP addresses that have recently connected to their network for any potential security threats. They have a list of 200 IP addresses and want to quickly identify any that might be malicious or suspicious.

1. The administrator prepares the `vt_results.txt` file with the 200 IP addresses.
2. They run the Tavily IP Checker using Docker.
3. The tool processes each IP address, querying the Tavily API for additional information.
4. A comprehensive report is generated, highlighting any IP addresses flagged as malicious or suspicious, along with detailed information about why they were flagged.
5. The administrator can quickly review the report and take appropriate action on any potentially harmful IP addresses.

## Sample Input and Output

### Sample Input (`vt_results.txt`):

IP: 192.168.1.1, Malicious: 0, Suspicious: 0
IP: 10.0.0.1, Error: API request failed
IP: 203.0.113.1, Malicious: 1, Suspicious: 0
IP: 198.51.100.1, Malicious: 0, Suspicious: 1
text

### Sample Output (`tavily_results_20240821_120000.txt`):

IP: 203.0.113.1 (Malicious: 1, Suspicious: 0)
Query: Why is IP 203.0.113.1 flagged as malicious or suspicious?
Answer: IP 203.0.113.1 is flagged as malicious due to its association with known malware distribution and botnet command and control activities. It has been reported by multiple threat intelligence sources for engaging in malicious behavior.
Query: What can be found about IP 203.0.113.1 in terms of cybersecurity aspects?
Answer: IP 203.0.113.1 has been identified as a high-risk address involved in various cybersecurity threats. It has been observed participating in DDoS attacks, hosting phishing websites, and distributing malware. The IP is listed on several reputable blacklists and has a history of abusive behavior dating back several months. IP: 198.51.100.1 (Malicious: 0, Suspicious: 1)
Query: Why is IP 198.51.100.1 flagged as malicious or suspicious?
Answer: IP 198.51.100.1 is flagged as suspicious due to anomalous network behavior and potential involvement in spam activities. While not confirmed as malicious, it has exhibited patterns consistent with compromised systems or botnets.
Query: What can be found about IP 198.51.100.1 in terms of cybersecurity aspects?
Answer: IP 198.51.100.1 has been observed engaging in suspicious activities such as port scanning and attempting to access known vulnerable services. It has also been associated with a higher-than-average volume of SMTP traffic, suggesting potential involvement in spam campaigns. While not definitively malicious, this IP warrants further investigation and monitoring. Summary of Flagged IPs:
IP: 203.0.113.1, Malicious: 1, Suspicious: 0
IP: 198.51.100.1, Malicious: 0, Suspicious: 1
IPs with Errors:
IP: 10.0.0.1, Error: API request failed
text

## Contributing

Contributions to improve Tavily IP Checker are welcome. Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
