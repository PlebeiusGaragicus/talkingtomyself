import os
import random
import logging
logger = logging.getLogger()

import pygame

from fishyfrens.config import *
from fishyfrens.app import App



class SoundMaster:
    """
        https://pixabay.com/music/search/game%20intro/?pagi=3
    """

    def __init__(self):
        self.dink_effect = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'dink.wav') )

        self.oww_effects = {}
        for player_name in ["myca", "charlie"]:
            for i in range(3):
                file_name = os.path.join(MY_DIR, 'resources', 'sounds', f'{player_name}oww{i}.wav')
                logger.debug(f"loading sound {file_name}")
                self.oww_effects[f'{player_name}oww{i}'] = pygame.mixer.Sound( file_name )

        self.boost_effect = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'boost.wav') )

        self.you_died_effect = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'mycagameover.wav') )

        self.current_track = None
        self.quiet = App.get_instance().manifest.get("quiet", False)

    def play_bg(self, track: int = 0):
        if self.quiet:
            return

        if track == self.current_track:
            return
        else:
            self.current_track = track

        if track == 0:
            self.background_music = pygame.mixer.music.load( os.path.join(MY_DIR, 'resources', 'sounds', 'music-epic.wav') )
            pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely
        elif track == 1:
            
            self.background_music = pygame.mixer.music.load( os.path.join(MY_DIR, 'resources', 'sounds', 'music-mindfulness.mp3') )
            pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely
        else:
            raise NotImplementedError(f"background music track {track} does not exist")


    def stop_bg(self):
        self.current_track = None
        pygame.mixer.music.stop()


    def dink(self):
        if self.quiet:
            return

        self.dink_effect.set_volume(0.4)
        self.dink_effect.play()
    
    def boost(self):
        if self.quiet:
            return

        self.boost_effect.set_volume(0.3) # TODO: set once in __init__???
        self.boost_effect.play()
    
    def oww(self, player_name: str):
        if self.quiet:
            return

        r = random.randint(0, 2)

        effect = f"{player_name}oww{r}"

        self.oww_effects[effect].set_volume(0.5)
        self.oww_effects[effect].play()


    def you_died(self):
        if self.quiet:
            return

        self.you_died_effect.set_volume(0.7)
        self.you_died_effect.play()



_audio = None

def audio() -> SoundMaster:
    global _audio
    if _audio is None:
        _audio = SoundMaster()
    return _audio
