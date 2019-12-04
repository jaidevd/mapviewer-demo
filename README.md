# Mapviewer Demo

This application demonstrate the use of [g1.mapviewer](https://learn.gramener.com/guide/mapviewer/),
Gramex's abstraction over [leaflet]() that creates common GIS visuals.

## Installation & Setup

1. Install gramex and its dependencies - see the [installation guide](install.md) for details.
2. To run the app, try

```bash
$ gramex
```
in the project folder and visit [http://localhost:9988](http://localhost:9988) in your browser.
You should see a webpage that looks like this:

![](assets/home.md)

## Usage

### Display a map

To display any map on the webapp, drop any GeoJSON file in the upload box,
and click the "Next" button. For example, doing this with the following sample files:

* [India](https://cloud.gramener.com/f/a495212a1028427c8c33/?dl)
* [Indian Parliamentary Constituencies](https://cloud.gramener.com/f/6b197ccfa1d4492c845b/?dl)
* [Maharashtra Assembly Constituencies](https://cloud.gramener.com/f/f29f705068e84fac8b69/?dl)

should produce the following maps respectively.

![](assets/india.png)

![](assets/india_pc.png)

![](assets/maha_ac.png)

### Display a choropleth

Below the map, you should see a set of controls, divided into two groups, as follows:

![](assets/controls.png)

You can use the left panel to plot a choropleth.
If the uploaded GeoJSON contains a scalar column, it can be used as a metric for the choropleth.
