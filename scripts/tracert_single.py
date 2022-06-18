"""
Visualized Tracerout for a single look up (Domain or IPv4).
"""
from icmplib import traceroute
from icmplib.exceptions import NameLookupError
from scripts.vis_utils import draw_points
from asyncio import run as asyncrun
from scripts.net_utils import geolocations


def single_lookup(domain_ip):
    """ Function for doing a specific traceroute look up and displaying it on the map. """

    try:
        trace_hops = traceroute(domain_ip)
    except NameLookupError:
        trace_hops = []

    if len(trace_hops) == 0:
        print("Invalid domain name / ip address.")
        return

    loc = asyncrun(geolocations(trace_hops))

    # print info
    for l in loc:
        if l[5] == "":
            print(f"{l[0]}\t{l[-1]}\t{l[6]} ({l[1]}, {l[2]})")
        else:
            print(f"{l[0]}\t{l[-1]}\t{l[5]} ({l[1]}, {l[2]})")

    print("If the map didn't open automatically, it also got saved as \"tracert-v_map.html\".")
    draw_points(loc, domain_ip)
    return
