"""
Utility functions regarding the handling for IP addresses, domain names
and interactions with the "ip-api.com" API.
"""
from aiohttp import ClientSession
import asyncio


""" check if IPv4 address is in a private address range """
def private_ipv4(ip):
   binary_ip = [bin(int(n))[2:].zfill(8) for n in ip.split('.')]
   # cases: 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12
   if (binary_ip[0] == '11000000' and binary_ip[1] == '10101000') or \
         binary_ip[0] == '00001010' or \
         (binary_ip[0] == '10101100' and binary_ip[1].startswith('0001')):
      return True

   else:
      return False


""" takes IPv4 address and return info of it using ip-api.com
   [number, country, city, latitude, longitude, organization, isp, ip] """
async def get_ipv4_location(session, ip, num):
   async with session.get("http://ip-api.com/json/" + str(ip)) as resp:
      info = await resp.json()
      if info["status"] != "success":
         return []
      return [str(num), info["country"], info["city"], info["lat"], info["lon"], info["org"], info["isp"], info["query"]]


""" async function for api calls to "ip-api.com" """
async def geolocations(hops):
   async with ClientSession() as session:
      reqs = []
      c = 0
      for h in hops:
         if private_ipv4(h.address):
            c += 1
            continue
         reqs.append(asyncio.ensure_future(get_ipv4_location(session, h.address, c)))
         c += 1
      return await asyncio.gather(*reqs)
