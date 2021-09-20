# tracert-v
Visualized traceroute using Python. 

This python script is intended to be run from the terminal. It uses [icmplib](https://github.com/ValentinBELYN/icmplib) for performing the traceroute.
_(Since this task needs root privileges, make sure to run the script with them. On Linux use `sudo -E python tracert-v`)_

It then queries [ip-api](https://ip-api.com) to reslove the found ip-addresses to geo-locations and further displays the route on a world map using [plotly](https://github.com/plotly/plotly.py).

Before running make sure all needed modules are installed: `pip install icmplib plotly aiohttp asyncio`

![Example Image](./example.png)
