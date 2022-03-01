from dash import Dash, dcc, html, Input, Output
import altair as alt
import dash_bootstrap_components as dbc

# Idea: 
# (1) Group data based on year, month, lat, long --> result: filter by tsunami
# (2) Size of tsumani circle in the middle of the ocean represents magnitude of tsunami
# (3) Countries affected by tsunami will be highlighted yellow
# (4) Interactive: tooltip (total damage)
# (5) Second order interaction: dependent on year and highlight by country. 

# Read in Tsunami Data.
tsunami = pd.read_tsv('data/util/tsunami.tsv')


# Creation of base world map
# If we have time to finesse our plot, see this website: https://towardsdatascience.com/make-beautiful-spatial-visualizations-with-plotly-and-mapbox-fd5a638d6b3c

world_map = alt.topo_feature(data.world_110m.url, 'countries')

map = alt.Chart(world_map).mark_geoshape(
    fill='#2a1d0c', stroke='#706545', strokeWidth=1).transform_lookup(
    lookup = 'id',
    from_ = alt.LookupData(tsunami, 'id', ['latitude', 'longitude']
)).encode(
    color = 'earthquake_magnitude:Q'
).project(type='equalEarth')

