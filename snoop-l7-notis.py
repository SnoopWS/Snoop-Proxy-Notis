import requests
import json
import os
import random
import time
import simplejson
import datetime
import ipaddress

data_url = "RPSURLGOESHERE"
ips_url = "THEIPSURLLOGGOESHERE"

def format_ips(ips_list):
    formatted_ips = []
    for ip in ips_list:
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.version == 4:
                formatted_ips.append(f"ip route add blackhole {ip}/32")
            elif ip_obj.version == 6:
                formatted_ips.append(f"ip -6 route add blackhole {ip}/128")
        except ValueError:
            print(f"Invalid IP address: {ip}")
    return "\n".join(formatted_ips)

while True:
    try:
        response = requests.get(data_url)
        data = response.json()

        totalRPS = int(data["TotalRPS"])
        blockedRPS = int(data["BlockedRPS"])
        bypassedRPS = int(data["BypassedRPS"])
        stage = data["Stage"]
    except simplejson.errors.JSONDecodeError:
        print("Error: Unable to parse JSON data. Retrying in 2 seconds...")
        time.sleep(2)
        continue

    def UtcNow():
        now = datetime.datetime.utcnow()
        return now.isoformat()

    if totalRPS > 7000:
        response = requests.get(ips_url)
        ips_data = response.json()
        challenge_ip_requests = ips_data["CHALLENGE_IP_REQUESTS"]

        id = random.randint(1, 50000)
        directory = "/root/attacks/"

        if not os.path.exists(directory):
            os.makedirs(directory)

        now = datetime.datetime.now()
        time_string = now.strftime("%H:%M:%S")
        filename = f"{time_string}-{id}-DDoS-Attack.json"
        output_path = os.path.join(directory, filename)

        formatted_ips = format_ips(challenge_ip_requests)
        with open(output_path, "w") as file:
            file.write(formatted_ips)

        print(f"Output file saved at: {output_path}")

        payload = {
          "embeds": [
              {
                  "title": "**:warning: Trunaction attempt detected. :warning:**\n\n",
                  "description": f"A Trunaction attempt executed on the proxy node request elevated over 7,000 r/s. To prevent this we logged every block request and their details to stop truncation.",
                  "url": "https://snoop.gay",
                  "color": 0,
                  "timestamp": UtcNow(),
                  "fields": [
                      {
                          "name": ":no_entry_sign: Blocked RPS:",
                          "value": f"```\n{blockedRPS}\n```",
                          "inline": False
                      },
                      {
                          "name": ":unlock: Bypassed RPS:",
                          "value": f"```\n{bypassedRPS}\n```",
                          "inline": False
                      },
                      {
                          "name": ":rocket: Total RPS:",
                          "value": f"```\n{totalRPS}\n```",
                          "inline": False
                      },
                      {
                          "name": ":microbe: Attack details logged:",
                          "value": f"```\n{output_path}\n```",
                          "inline": False
                      },
                      {
                          "name": ":flag_ca: Stage:",
                          "value": f"```\n{stage}\n```",
                          "inline": False
                      }

                  ],
                  "author": {
                      "name": "\n Automated Capture \n",
                      "url": "https://cdn.discordapp.com/attachments/1116946927519551594/1119633602091688006/image-removebg-preview.png",
                      "icon_url": "https://cdn.discordapp.com/attachments/1116946927519551594/1119633602091688006/image-removebg-preview.png",
                      },
                      "footer": {
                          "text": "\n We have detected a truncation attempt. Snoop-Proxy v.1.03  \n",
                          "icon_url": "https://cdn.discordapp.com/attachments/947543840401817670/973423061829316658/download.gif?size=4096",
                      },
                      "image": {
                          "url": "https://cdn.discordapp.com/attachments/947543840401817670/973422297882976317/standard_11.gif?size=4096"
                      },
                      "thumbnail": {
                          "url": "https://cdn.discordapp.com/attachments/1116946927519551594/1119633602091688006/image-removebg-preview.png"
                      }
                  }
              ]
          }

        webhook_url = "https://discord.com/api/webhooks/1116946947530571876/iGtoWyzK-2uiZdAcclBkA32rMpGVF3TxlZ8greE0GscDDvavfgdR25Y8qEYSC-haX0d2"
        requests.post(webhook_url, json=payload)

        print("Alert sent to Discord")
        time.sleep(30)
    else:
        time.sleep(5)