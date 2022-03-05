# Reflections for Milestone 2

*By **DSCI 532 Group 11***

## What we have implemented
In this milestone, we have attempted to create three plots. 
First, a map plot highlighting the intensity of earthquakes and the countries that were affected by the tsunami (underwater earthquakes).
Second, a scatter plot to plot the trend of the earthquakes according to its intensity on the Richter Scale.
Third, a bar chart to highlight the top 10 tsunamis with the highest tsunami intensity of a given time period. (This is different from the earthquake intensity on the Richter Scale).

To use this dashboard, the user will be able to toggle the specific years and countries that they will like to examine on the left sidebar. 
The default argument for the time period for all three plots will from 1802 to 2022. 
The default argument for the countries for the map plot and scatter plot will be all countries. 
The scatter plot will highlight the top 10 countries from 1802 to 2022.

The bar chart will only take in the values for the years, and not the countries as it 
will display the top 10 most intense tsunamis across the world based on time period specified. 

## What could be improved
The structure of the dashboard needs to be improved greatly to make it more streamlined. Moreover, we would like to increase the functionality of the sidebar where users can collapse it,
such that the plot is rendered larger. Moreover, we would like to add a buttom besides the scatter plot and bar chart, to inform readers about how to interpret the 'Richter Scale' and 'Tsunami Intensity'.

The convention of the naming of the functions within each component can also be improved, to allow future collaborators to understand our code with ease.