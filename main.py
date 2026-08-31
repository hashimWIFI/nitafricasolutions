import os
import http.server
import json
import urllib.request

PORT = int(os.environ.get("PORT", 8080))
# Aligned to your exact Railway variable names (TXTBEE)
TEXTBEE_API_KEY = os.environ.get("TXTBEE_API_KEY")
TEXTBEE_DEVICE_ID = os.environ.get("TXTBEE_DEVICE_ID")

class TextBeeWebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
            customer_number = payload.get('from')
            incoming_message = payload.get('message', '')
            
            print(f"📩 Incoming request from {customer_number}: '{incoming_message}'")
            
            if customer_number and TEXTBEE_API_KEY and TEXTBEE_DEVICE_ID:
                api_url = f"https://textbee.dev{TEXTBEE_DEVICE_ID}/sendSync-sms"
                
                reply_payload = json.dumps({
                    "recipients": [customer_number],
                    "message": "Your secure transaction voucher PIN code is: 8492"
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    api_url, 
                    data=reply_payload, 
                    headers={
                        'Content-Type': 'application/json',
                        'x-api-key': TEXTBEE_API_KEY
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req) as response:
                    print(f"🚀 Outgoing Voucher text triggered via Samsung device. Status: {response.getcode()}")
            
            self.send_response(200)
            self.end_headers()
            
        except Exception as e:
            print(f"❌ Automation Error: {e}")
            self.send_response(500)
            self.end_headers()

def run():
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, TextBeeWebhookHandler)
    print(f"🤖 Production cloud bot is live on port {PORT}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
