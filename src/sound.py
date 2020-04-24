#!/usr/bin/env python3
# coding: utf8
import enum, numpy, random, pyxel
from abc import ABCMeta, abstractmethod

class Sound:
    def __init__(self):
        self.scale = IonianScale()
        self.is_mute = False
    def sound(self, mino_id):
        if self.is_mute: return
        notes = Note.get(self.scale.Keys[mino_id])
        tone = 'p'
        volume = '6'
        effect = 'f'
        speed = 30
#        print(notes)
        sound_bank = 0
        pyxel.sound(sound_bank).set(
            notes,
            tone,
            volume,
            effect,
            speed,
        )
        channel = 0
        pyxel.play(channel, sound_bank)
    def increment_key(self):
        self.scale.increment_key()
    def decrement_key(self):
        self.scale.decrement_key()
    def toggle_mute(self):
        if self.is_mute: self.is_mute = False
        else: self.is_mute = True
    @property
    def IsMute(self): return self.is_mute

class Key:
    Min = 0
    Max = 11
    Len = 12
    Names = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

class IonianScale: # https://ja.wikipedia.org/wiki/%E9%9F%B3%E9%9A%8E
    def __init__(self):
        self.key = 0
        self.intervals = (0, 2, 4, 5, 7, 9, 11)
    @property
    def Key(self): return self.key
    @Key.setter
    def Key(self, value):
        if Key.Min <= value <= Key.Max: self.key = value
    @property
    def Keys(self): return [i+self.key for i in self.intervals]
    def increment_key(self):
        if Key.Max < self.key: self.key = Key.Min
    def decrement_key(self):
        if self.key < Key.Min: self.key = Key.Max

class Note:
    @staticmethod
    def get(note):
        key = note % 12
        pitch = 1 + (note // 12)
        return Key.Names[key] + str(pitch)

if __name__ == '__main__':
    class App:
        def __init__(self):
            pyxel.init(10,10)
            Sound().sound(0)
            pyxel.run(self.update, self.draw)
        def draw(self): pyxel.cls(0)
        def update(self): pass
    App()

