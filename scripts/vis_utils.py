"""
Utility functions regarding the visualization using plotly.
"""
import plotly.graph_objects as go


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
         color='red',
      )
   ))

   # drawing lines
   fig.add_trace(go.Scattergeo(
      lon=lons,
      lat=lats,
      hoverinfo='text',
      text=names,
      mode='lines',
      line=dict(width=1, color='red')
   ))

   # adjusting design of the map
   fig.update_layout(
      title_text=f'Traceroute for \"{inp}\"',
      showlegend=False,
      geo=dict(
         resolution=110, scope="world",
         showland=True, landcolor="Gray",
         showocean=True, oceancolor="Black",
         showlakes=True, lakecolor="Black",
         showcountries=True, countrycolor="White"
      ),
      margin_b=0,
      margin_l=0,
      margin_r=0,
      margin_t=50
      # width=,
      # height=
   )

   fig.update_geos(fitbounds="locations")
   fig.write_html('tracert-v_map.html')
   fig.show()
   return
