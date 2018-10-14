#! /usr/bin/python
import json

import requests

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

email = config['email']
key = config['key']
zone = config['zone']
record = config['record']


def ipify():
    r = requests.get("https://api.ipify.org/")
    r.raise_for_status()
    return r.text


class Cloudflare:
    def __init__(self, email, key):
        self.endpoint = "https://api.cloudflare.com/client/v4"
        self.headers = {'X-Auth-Email': email, 'X-Auth-Key': key, 'Content-Type': 'application/json'}

    def user(self):
        r = requests.get(self.endpoint + "/user", headers=self.headers)
        return r.json()

    def zones(self, zone):
        payload = {'name': zone}
        r = requests.get(self.endpoint + "/zones", headers=self.headers, params=payload)
        return r.json()

    def dns_records(self, zone_id, record):
        payload = {'name': record}
        r = requests.get(self.endpoint + "/zones/" + zone_id + "/dns_records", headers=self.headers, params=payload)
        return r.json()

    def update_record(self, zone_id, record_id, record, ip_address):
        payload = {'type': 'A', 'name': record, 'content': ip_address}
        r = requests.put(self.endpoint + "/zones/" + zone_id + "/dns_records/" + record_id, headers=self.headers, data=json.dumps(payload))
        return r.json()


cf = Cloudflare(email, key)
zone_id = cf.zones(zone)['result'][0]['id']
record_id = cf.dns_records(zone_id, record)['result'][0]['id']

ip_address = ipify()

print(cf.update_record(zone_id, record_id, record, ip_address))
