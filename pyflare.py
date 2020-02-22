#! /usr/bin/python
import json, os

import requests

class Cloudflare:
    def __init__(self, email, key):
        self.endpoint = "https://api.cloudflare.com/client/v4"
        self.headers = {'X-Auth-Email': email, 'X-Auth-Key': key, 'Content-Type': 'application/json'}

    def getmyip(self):
        r = requests.get("https://api.ipify.org/")
        return r.text

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

    def update_record(self, zone_id, record_id, record, ttl, ip_address, proxied):
        payload = {'type': 'A', 'name': record,'ttl': ttl, 'content': ip_address, 'proxied': proxied}
        r = requests.put(self.endpoint + "/zones/" + zone_id + "/dns_records/" + record_id, headers=self.headers, data=json.dumps(payload))
        return r.json()

    def __call__(self,zone,record,ttl,proxied):
        zone_id = cf.zones(zone)['result'][0]['id']
        record_id = cf.dns_records(zone_id, record)['result'][0]['id']
        ip_address = cf.getmyip()
        if ip_address != cf.dns_records(zone_id, record)['result'][0]['content']:
            return cf.update_record(zone_id, record_id, record, ttl, ip_address, proxied)
        else:
            return "Record is up-to-date"

if __name__ == '__main__':
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	try:
		with open(os.path.join(__location__,'config.json')) as json_data_file:
			config = json.load(json_data_file)
			email = config['email']
			key = config['key']
			zone = config['zone']
			record = config['record']
			ttl = config['ttl']
			proxied = config['proxied']

		cf = Cloudflare(email, key)
		print(cf(zone,record,ttl, proxied))
	except IOError:
		print("Unable to find config file.")

