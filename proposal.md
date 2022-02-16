# Proposal

## Motivation and Purpose

Our role: Tsunami data science enthusiasts

Target Audience: Fellow tsunami enthusiasts

Vancouver sits on the edge of the Pacific Rim of Fire - a region where most of the volcanic eruptions and earthquakes occur. These eruptions occur in the middle of the Pacific Ocean and travel towards land as tsunamis. Each varies in magnitude and location and causes physical and economic damage. How do we track each tsunami that has occurred? How do we know how the magnitude of tsunamis changes over time? How can we compare the damage of each tsunami to another in the same year or between countries?

To address these questions, we propose building a data visualisation app that allows these enthusiasts to visually explore a dataset of past tsunami instances over the past few hundred years (the data set consist of tsunamis from 2100BC, but we have decided to limit it to 1800AD). Our app will show how the distribution of tsunamis vary over time, and users can use the tooltip to find our more information about each tsunami. It will also list the top 10 tsunamis that occur in the given time period that the use has selected.

## Description

We will be visualizing 2167 tsunami instances (out of the possible 2767 instances). While the dataset has many associated variables, the key variables are as follows. Each tsunami instance has time information (`Year`, `Mo`, `Dy`, `Hr`, `Mn`, `Sec`), geographical position (`Country`, `Location Name`, `Latitude`, `Longitude`), hydrological condition (`Maximum Water Height`, `Earthquake Magnitude`), and damage (`Total Deaths`, `Total Injuries`, `Total Missing`, `Total Damage ($Mil)`, `Total Houses Destroyed`).

## Research Questions and Usage Scenarios