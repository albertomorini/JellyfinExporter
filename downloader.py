import requests

headers = {'Authorization': 'MediaBrowser Client="Jellyfin%20Web", Device="Firefox", DeviceId="TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTAuMTU7IHJ2OjEzNS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEzNS4wfDE3NDA1MTgwNTk1NjE1", Version="10.10.6", Token="cd00993a7bfe4b2caccc288aedf170aa"'}

res = requests.get("http://10.0.0.3:8096/Items/68a3a384293fe8359461c907a046ef27/Download", headers=headers)

print(res.status_code)
print(res.headers["filename"])

if(res.status_code==200):
    f = open("./NAME.m4a","w")
    f.write(res)
    f.close