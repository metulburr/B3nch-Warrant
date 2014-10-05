
import pygame as pg
from ... import tools

class Part1(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.next = "PART2"

        self.set_cover()

        self.image_orig = tools.Image.load('mailman.jpg')
        self.image = pg.transform.scale(self.image_orig, (200,250))
        self.image_rect = self.image.get_rect(center=self.screen_rect.center)
        self.set_blinker_text()
        self.set_blinker()
        self.set_message()
        self.is_typing = False
        self.is_playing_music = False
        
    def set_blinker_text(self):
        text = ['Press Any Key']
        y = self.screen_rect.bottom - 100
        self.rendered_text = self.make_text_list("Fixedsys500c",25,text,(255,0,0),y,0)
        
    def set_blinker(self):
        self.blink = False
        self.blink_time = 1.0
        self.blink_timer = 0
            
    def set_message(self):
        self.msg_time = 1.0
        self.msg_timer = 0
        self.msg_index = 0
        self.message_complete = False
        self.type_message()
        
    def set_cover(self):
        self.cover = pg.Surface((self.screen_rect.width, self.screen_rect.height))
        self.cover.fill(0)
        self.cover_alpha_orig = 256
        self.cover_alpha = self.cover_alpha_orig
        self.alpha_step = 3

    def make_text_list(self,font,size,strings,color,start_y,y_space):
        rendered_text = []
        for i,string in enumerate(strings):
            msg = self.render_font(font,size,string,color)
            rect = msg.get_rect(center=(self.screen_rect.centerx,start_y+i*y_space))
            rendered_text.append((msg,rect))
        return rendered_text

    def render_font(self,font,size,msg,color=(255,255,255)):
        selected_font = tools.Font.load('impact.ttf', size)
        return selected_font.render(msg,1,color)
        
    def type_message(self):
        message = 'Congratulations!'
        self.message_image, self.message_image_rect = self.make_text(message[:self.msg_index],(255,0,0),self.screen_rect.center,44)
        if self.msg_index >= len(message):
            self.message_complete = True

    def update(self,surface,keys):
        self.current_time = pg.time.get_ticks()
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        if self.message_complete:
            self.typing.sound.stop()
            if self.current_time-self.blink_timer > 1000/self.blink_time:
                self.blink = not self.blink
                self.blink_timer = self.current_time
        if self.current_time-self.msg_timer > 200/self.msg_time:
            self.msg_timer = self.current_time
            if self.cover_alpha < 1:
                self.msg_index += 1
                self.type_message()
                if not self.is_typing:
                    self.typing.sound.play()
                    self.is_typing = not self.is_typing
            
    def render(self, screen):
        screen.fill((255,255,255))
        screen.blit(self.image, self.image_rect)
        screen.blit(self.message_image, self.message_image_rect)
        screen.blit(self.cover,(0,0))
        if self.blink:
            for msg in self.rendered_text:
                screen.blit(*msg)

    def get_event(self,event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            self.done = True
            
    def cleanup(self):
        self.typing.sound.stop()
        
    def entry(self):
        self.set_cover()
        self.set_message()
        self.set_blinker()
        self.bg = pg.transform.scale(self.image, (self.screen_rect.width, self.screen_rect.height))
        self.bg_rect = self.bg.get_rect(center=self.screen_rect.center)
        if not self.is_playing_music:
            pg.mixer.music.play()
            self.is_playing_music = not self.is_playing_music
