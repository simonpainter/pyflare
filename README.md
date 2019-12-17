# pyflare
Updates Cloudflare with current IP

In addition to many other benefits, Cloudflare will host your DNS for free. This script provides an alternative to dynamic dns services by leveraging Cloudflare's API. It does this by taking your current IP and updating Cloudflare's DNS records. In doing so, Cloudflare will always point to your correct IP even as it changes.

Inspiration: https://www.reddit.com/r/raspberry_pi/comments/9nimtz/use_cloudflare_as_dynamic_dns_with_raspberry_pi/


# Prerequisites
You must have a Cloudflare account with one domain (zone) available. This script will update the records associated with this zone.
* Create an account with Cloudflare
* Set up at least one domain with them
* When logged in, go to your Profile > API Tokens > Create Token
* During token creation, enable permissions "Zone.Zone.Settings" and "Zone.Zone," and "Zone.DNS" with resources "All Zones"


# config.json

Create a file named "config.json" in the same directory as pyflare.py. This file should be formatted as JSON. For multiple records, create a list (or array) of dictionaries (objects) containing your parameters.

```
[
	{
		"email": "<YOUR CLOUDFLARE EMAIL ADDRESS>",
		"key": "<YOUR CLOUDFLARE API KEY>",
		"zone": "<THE DNS ZONE CONTAINING THE RECORD TO BE UPDATED (e.g. domain.com)>",
		"record": "<THE SPECIFIC RECORD TO UPDATE (e.g. api.domain.com)>"
	}
]
```
