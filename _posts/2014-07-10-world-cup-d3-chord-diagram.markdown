---
layout: post
title:  "Where do the World Cup squads play Club football?"
date:   2014-07-10 11:55
categories: data
tags: data, d3, visualisation
permalink: /:year/:month/:title 
---

The Guardian have released some great data on the 2014 FIFA World Cup squads. As the tournament draws to a close, I've taken a look at where the players play their club football.

# Players by Club Country

<iframe width="1000" height="1000" src="http://jsfiddle.net/benunsworth/FtFB2/embedded/result,js/" frameborder="0"> </iframe>

I've borrowed from the Mike Bostock [Uber Rides visualisation](http://bost.ocks.org/mike/uberdata/) and [delimited.io](http://www.delimited.io/). The chord diagram is a great way to look at relationships between data.

In this example I've used a pivot table to build a matrix representing "country plays for" and "country plays club football in". If you click on the JavaScript tab of the embed above you can see this data.

The matrix of data is associated with the Country's represented at this year's World Cup, the [D3 library](http://d3js.org/) performs it's magic and the chord diagram is born.

# What does the diagram show?

If a data visualisation is doing it's job, it should be easy to see the story.

The width of the band at each country name show how many players at the world cup play their club football in that country.

If you hover over the band with the country name you can see the flow of players in and out of a country. Hovering on my country, England, shows that no English Squad players play their club football in any other 2014 World Cup nation - but lots of other international players do play their club football in the English leagues.

# Note about the data

The D3 chord diagram requires a square matrix, in this case a 32 x 32 matrix of 2014 FIFA World Cup Teams. There are players at the world cup who play their club football in countries not at this year's world cup. This is not represented in the diagram.

# Things to improve
- Parse the data programmatically, rather than dumping the matrix into the code
- Rotate country labels and place outside the diagram, to improve legibility
- Make better use of colour to represent data flow, right now it's purely asthetic
