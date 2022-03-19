# Reflections for Milestone 4

*By **DSCI 532 Group 11***

## Introduction

We tried to make both our DashR and DashPy apps as similar as possible but still there might be some minor noticeable differences. We perfected the UI as much as possible to be aesthetically pleasing which is one of the positive comments we recieved for our app. We tried our best to incorporate all the valuable feedback from the TA and peers.

> In the dataset, there are many valid tsunami records which don't have values in the columns `Total Deaths` and `Tsunami Intensity`. So, even if the map plot shows some records, the scatter and bar plots might be empty. We would like to confirm that it's not a bug and it's because of the nature of the data.

## Differences

### 1. Scatter plot greying effect

One of the differences between our DashR and DashPy apps has to do with display of the scatter plot of earthquake magnitude to total deaths. In both apps, this plot responds to user specified changes to the years and magnitude sliders as well as the country selection drop-down menu. In addition, in an attempt to enhance user interpretability of this plot, we intended to grey out events that did not fall within the selected magnitude range, while colouring selected events by their the top 10 countries registering strong magnitude events.

We were able to produce this output in R thanks ggplot’s flexible chart layering convention. However, we were not able to achieve the same result in Python due to Altair’s known inability to layer observations from two plots that use distinct color configurations. Hence, the Python scatter plot only displays events that match the selection of the earthquake slider.

### 2. Zoom Functionality in Python

Altair's backend **vega** doesn't not support zoom in and zoom out functionality in `mark_geoshape` yet and hence we were not able to include that in out DashPy app whereas we were able to accomplish that with plotly in DashR easily.

### 3. Tsunami Origin Legend

We were not able to add legend for tsunami origin red dots in our DashR map plot, this is because plotly scatter plot does not support showing legend for a single color value like "red". It shows only when we encode color with a column. We were able to accomplish this in our DashPy app.

## Improvements

There are a lot of ways in which we can improve our apps. One of them would be to add information buttons to the plot borders, so that the user can click them to know more information about the plots.