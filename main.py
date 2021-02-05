import requests
import toml
import api_reader

config_data = toml.load("configuration.toml")

base_url = config_data.get("api").get("base")
api_key = api_reader.get_api_key(not config_data.get("misc").get("silence_key_in_console"))

print("[Local] Generating auth headers")
auth_headers = {'Authorization': f'Bearer {api_key}'}

print("[Local] Sending Request")
resp = requests.get(url=f"{base_url}user/tokens/verify", headers=auth_headers)
data = resp.json()

messages = data.get("messages")

for message in messages:
    print(f"[Remote] [{message.get('code')}] {message.get('message')}")

if not data.get("success"):
    print("[Local] Server Responded with no success. Quitting.")
    quit()

print("[Local] Getting IPv4 Address")
ipv4api = "https://api.ipify.org/?format=json"
ipv4_resp = requests.get(url=ipv4api)
ipv4_resp = ipv4_resp.json()
ipv4_resp = ipv4_resp.get("ip")

print("[Local] Server responded with ip address " + ipv4_resp)
print("[Local] Starting Actions")
for action in config_data.get("actions").get("zone_identifiers"):
    print("[Local] Starting action for " + action)
    # Collect data
    dns_records = requests.get(f"{base_url}zones/{action}/dns_records", headers=auth_headers)
    dns_json = dns_records.json()
    if not dns_json.get("success"):
        print("[Local] Server responded with no success, going to next action.")
        continue

    result_list = dns_json.get("result")
    for record in result_list:
        if record.get("type") == "A":
            print("[Local] Record with type 'A' detected. Changing to current ip address.")
            try:
                resp = requests.put(f"{base_url}zones/{action}/dns_records/{record.get('id')}", json={"type": "A", "name": record.get("name"), "content": ipv4_resp, "ttl": record.get("ttl"), "proxied": record.get("proxied")}, headers=auth_headers)
                if resp.json().get("success"):
                    print("[Local] Success!")
                else:
                    print("[Local] Failure")
                    for error in resp.json().get("errors"):
                        print(f"[Remote] [{error.get('code')}] {error.get('message')}")
            except Exception as e:
                print(f"[Local] [FATAL] {e} while sending request to change to current ip address")
                continue