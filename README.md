# tracert-v

Visualized traceroute using Python. This python script is intended to be run from the terminal. It uses [icmplib](https://github.com/ValentinBELYN/icmplib) for performing the traceroute. It then queries [ip-api](https://ip-api.com) to resolve the found ip-addresses to geo-locations and further displays the route on a world map using [plotly](https://github.com/plotly/plotly.py). To find all open connections it sniffs packets using [scapy](https://github.com/secdev/scapy).

Before running make sure all needed modules are installed: `pip install icmplib plotly aiohttp asyncio scapy dash`

![Example Image](./example.png)

## How to use

`python3 tracert-v.py {domain or IPv4 address}` for looking up one specific route

`python3 tracert-v.py all {seconds to run [int]}` for sniffing all open connections over the given time

### Remark

IP addresses in the private address space are filtered out from the look ups.

## Possible Issues

* The "traceroute" function from icmplib needs **root privileges**, make sure to run the script with them. (On Linux use `sudo -E python3 tracert-v.py` and on Windows run "cmd" as administrator.)

* If you only see the last hop of traceroutes, this might have to do with your firewall settings (see [icmplib issue](https://github.com/ValentinBELYN/icmplib/issues/10)).  To fix this add/edit the rule in your firewall to **allow incoming ICMPv4/ICMPv6 "timeout" and "destination unreachable" packets**.
