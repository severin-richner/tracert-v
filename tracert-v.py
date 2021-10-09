"""
Visualized Traceroute script.
author: severin-richner
date:   09.10.21
"""

from icmplib import traceroute
from icmplib.exceptions import NameLookupError
from aiohttp import ClientSession
import plotly.graph_objects as go
from sys import argv
import asyncio


def private_ip(ip):
    """ check if ip address is in a private address range """
    binary_ip = [bin(int(n))[2:].zfill(8) for n in ip.split('.')]

    # cases: 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12
    if (binary_ip[0] == '11000000' and binary_ip[1] == '10101000') or \
            binary_ip[0] == '00001010' or \
            (binary_ip[0] == '10101100' and binary_ip[1].startswith('0001')):
        return True
    else:
        return False


async def get_ip_location(session, ip, num):
    """ takes IPv4 address and return info of it using ip-api.com
        number, country, city, latitude, longitude, organization, isp, ip """

    async with session.get("http://ip-api.com/json/" + str(ip)) as resp:
        info = await resp.json()
        if info["status"] != "success":
            return []
        return [str(num), info["country"], info["city"], info["lat"], info["lon"], info["org"], info["isp"],
                info["query"]]


async def geolocations(hops):
    """ async function for api calls to "ip-api.com" """

    async with ClientSession() as session:

        reqs = []
        c = 0
        for h in hops:

            if private_ip(h.address):
                c += 1
                continue

            reqs.append(asyncio.ensure_future(get_ip_location(session, h.address, c)))
            c += 1

        return await asyncio.gather(*reqs)


def draw_points(loc_info, inp):
    """ draws the line on the world map and displays it """

    lats = [x[3] for x in loc_info]
    lons = [x[4] for x in loc_info]
    names = [f"{x[0]}: {x[6]} ({x[1]}, {x[2]})" for x in loc_info]

    fig = go.Figure()

    # drawing markers
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='markers',
        marker=dict(
            size=5,
            color='rgb(255, 0, 0)',
        )
    ))

    # drawing lines
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        hoverinfo='text',
        text=names,
        mode='lines',
        line=dict(width=1, color="red")
    ))

    # adjusting desgin of the map
    fig.update_layout(
        title_text=f'Traceroute for \"{inp}\"',
        showlegend=False,
        geo=dict(
            resolution=110, scope="world",
            showland=True, landcolor="Gray",
            showocean=True, oceancolor="Black",
            showlakes=True, lakecolor="Black",
            showcountries=True, countrycolor="White",
        )
    )

    fig.update_geos(fitbounds="locations")
    fig.write_html('tracert-v_map.html')
    fig.show()


def single_lookup(domain_ip):
    """ Function for doing a specific traceroute look up and displaying it on the map. """

    try:
        trace_hops = traceroute(domain_ip)
    except NameLookupError:
        trace_hops = []

    if len(trace_hops) == 0:
        print("Invalid domain name / ip address.")
        return

    loc = asyncio.run(geolocations(trace_hops))

    # print info
    for l in loc:
        if l[5] == "":
            print(f"{l[0]}\t{l[-1]}\t{l[6]} ({l[1]}, {l[2]})")
        else:
            print(f"{l[0]}\t{l[-1]}\t{l[5]} ({l[1]}, {l[2]})")

    print("If the map didn't open automatically, it also got saved as \"tracert-v_map.html\".")
    draw_points(loc, domain_ip)
    return


def all_connections():
    #TODO
    return


if __name__ == "__main__":
    """ main function """

    if len(argv) == 1 or len(argv) > 2:
        print("Invalid argument. Possible arguments: {Domain/IPv4 address}, all")
        exit()

    user_in = str(argv[1]).lower()

    if user_in == "all":
        all_connections()

    else:
        single_lookup(user_in)
