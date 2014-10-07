#!/usr/bin/env python

import pygame as pg
from data.main import main
import data.tools
import argparse
import sys
from data.tools import DB

DEFAULT = { 
        'fullscreen':False,
        'difficulty':'medium',
        'size'      :(800,600),
        'caption'   :'B3nch Warrant',
        'resizable' :False,
        'resolution_options': [(640,360), (800,600), (854,480), (1280,720)],
        'save':{
            'won':0,
            'lost':0,
            'points':0,
            'shortest':None,
        },
}

parser = argparse.ArgumentParser(description='{} Arguments'.format(DEFAULT['caption']))
parser.add_argument('-c','--clean', action='store_true', 
    help='Remove all .pyc files and __pycache__ directories')
args = vars(parser.parse_args())

if __name__ == '__main__':
    if args['clean']:
        data.tools.clean_files()
    else:
        if not DB.exists():
            DB.save(DEFAULT)
            db = DEFAULT
        else:
            db = DB.load()
        print(db)
        main(**db)
    pg.quit()

