import pandas as pd
import os.path as op
import json
import numpy as np
from geopandas import read_file
import shutil

DIR = op.join(op.dirname(__file__), 'uploads')

cache = {}


def find_neighbors(gdf):
    neighbors = {}
    for ix, rowdata in gdf.iterrows():
        neighbors[ix] = gdf.index[gdf['geometry'].intersects(rowdata.geometry)]
    return neighbors


def choropleth(handler):
    df = pd.read_json('metadata.json')
    col = handler.path_args[0]
    X = df[col]
    X = (X - X.min()) / (X.max() - X.min())
    X = np.digitize(X.values, np.linspace(0, 1, 20))
    df[col + '_norm'] = X
    df.to_json(op.join(DIR, 'metadata.json'), orient='records')


def get_lis(handler):
    gcol, mcol, ccol = handler.path_args
    gdf = cache.get('gdf')
    if gdf is None:
        gdf = cache['gdf'] = read_file(op.join(DIR, 'map.geojson'))
    df = cache.get('df')
    if df is None:
        df = cache['df'] = pd.read_csv(op.join(DIR, 'meta.csv'))
    gdf.set_index(gcol, inplace=True, verify_integrity=True, drop=False)
    df.set_index(mcol, inplace=True, verify_integrity=True, drop=False)
    neighbors = find_neighbors(gdf)
    gdf['lis_score'] = 0
    for ix, rowdata in df.iterrows():
        if ix in neighbors:
            winner = rowdata[ccol]
            xdf = df.loc[neighbors[ix], ccol]
            gdf.loc[ix, 'lis_score'] = (xdf == winner).sum() / xdf.shape[0]
    out = gdf[['lis_score', 'AC_NAME']].reset_index()
    out.to_json(op.join(DIR, 'lis.json'), orient='records')
    return "OK"


def process_upload(meta, handler):
    fpath = op.join(DIR, meta.file)
    if meta.mime == 'text/csv':
        outpath = op.join(DIR, 'meta.csv')
        cache['df'] = pd.read_csv(fpath)
        df = cache['df']
        with open(op.join(DIR, 'metacols.json'), 'w') as fout:
            json.dump([''] + df.columns.tolist(), fout, indent=4)
        df.to_json('metadata.json', orient='records')
    elif meta.mime in ('application/geo+json', 'application/json'):
        outpath = op.join(DIR, 'map.geojson')
        cache['gdf'] = read_file(fpath)
        gdf = cache['gdf']
        gcols = [''] + gdf.columns.tolist()
        gcols.remove('geometry')
        with open(op.join(DIR, 'gcols.json'), 'w') as fout:
            json.dump(gcols, fout, indent=4)
    else:
        print(meta.mime)
    shutil.move(fpath, outpath)
