

import pygame as pg
from .. import tools
from ..toolbox import button
import os
import random
from data.tools import DB

class Game(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        
        self.screen_rect = screen_rect
        self.bg_color = (255,255,255)
        self.setup_btns()

        self.timer = 0
        self.best = DB.load()['save']['shortest']
        self.update_label()

        self.overlay_orig = pg.Surface((screen_rect.width, screen_rect.height))
        self.set_overlay()
        
        self.bg_orig = tools.Image.load('courtroom.jpg')
        self.bg = pg.transform.scale(self.bg_orig, (self.screen_rect.width, self.screen_rect.height))
        self.bg_rect = self.bg.get_rect(center=self.screen_rect.center)
        
    def set_overlay(self):
        self.overlay = pg.transform.scale(self.overlay_orig, (self.screen_rect.width, self.screen_rect.height))
        self.overlay.fill(0)
        self.overlay.set_alpha(200)
        
    def update_label(self):
        
        text = "Turns: "
        self.turns_text, self.turns_rect = self.make_text(text, (0,0,0), (60, 125), 20)
        
        
    def setup_btns(self):
        self.buttons = []
        
        button_config = {
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (205,195, 0),
            'font'               : tools.Font.load('impact.ttf', 18),
            'font_color'         : (255,255,255),
            'border_color'       : (0,0,0),
        }
        c = (0,0,0) #clicked color for color buttons

        self.issue_warrant_button = button.Button((10,10,105,25),(0,0,100), 
            self.issue_warrant, text='Issue Warrant', clicked_color=(255,255,255), 
            hover_color=(0,0,130), **button_config
        )
        self.deny_warrant_button = button.Button((10,50,105,25),(0,0,100), 
            self.deny_warrant, text='Deny Warrant', clicked_color=(255,255,255), 
            hover_color=(0,0,130), **button_config
        )
        
        self.buttons += [
                self.issue_warrant_button, self.deny_warrant_button
        ]
        
    def issue_warrant(self):
        pass
        
    def deny_warrant(self):
        pass
        
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == self.keybinding['back']:
                self.button_click.sound.play()
                self.done = True
                self.next = 'MENU'
                
        self.switch_track_event(event)
        for button in self.buttons:
            if not button.disabled:
                button.check_event(event)
        #self.menu_button.check_event(event)
                    
    def update(self, now, keys):
        self.update_label()
            
        if pg.time.get_ticks()-self.timer > 1000:
            self.timer = pg.time.get_ticks()
            pass
        
    def render(self, screen):
        screen.fill((self.bg_color))
        screen.blit(self.bg, self.bg_rect)
        screen.blit(self.overlay, self.bg_rect)
        for button in self.buttons:
            button.render(screen)

        #self.menu_button.render(screen)

    def load_save(self):
        db = DB.load()
        self.games_won = db['save']['won']
        self.games_lost = db['save']['lost']
        self.points = db['save']['points']
        
    def write_save(self):
        db = DB.load()
        db['save']['won'] = self.games_won
        db['save']['lost'] = self.games_lost
        db['save']['points'] = self.points
        DB.save(db)

    def cleanup(self):
        pass
        
    def entry(self):
        self.bg = pg.transform.scale(self.bg_orig, (self.screen_rect.width, self.screen_rect.height))
        self.bg_rect = self.bg.get_rect(center=self.screen_rect.center)
        self.set_overlay()
