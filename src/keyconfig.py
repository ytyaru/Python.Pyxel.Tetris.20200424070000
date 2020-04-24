#!/usr/bin/env python3
# coding: utf8
import os, csv, enum, numpy, random, pyxel
from abc import ABCMeta, abstractmethod

class ActType(enum.IntEnum):
    MoveL = 0
    MoveR = 1
    RollL = 2
    RollR = 3
    SpeedUp = 4
    Fall = 5

class KeyConfig:
    def __init__(self):
        self.name = 'Default'
        self.keys = [0] * len(ActType)
        self.keys[ActType.MoveL] = pyxel.KEY_LEFT
        self.keys[ActType.MoveR] = pyxel.KEY_RIGHT
        self.keys[ActType.RollL] = pyxel.KEY_L
        self.keys[ActType.RollR] = pyxel.KEY_R
        self.keys[ActType.SpeedUp] = pyxel.KEY_DOWN
        self.keys[ActType.Fall] = pyxel.KEY_SPACE
    @property
    def Name(self): return self.name
    @Name.setter
    def Name(self, value):
        if isinstance(value, str) and 0 < len(value.strip()): self.name = value
    @property
    def Keys(self): return self.keys
    def set(self, typ, value):
        if not isinstance(typ, (int, ActType)): return
        if not 0 <= value <= 138: return
        self.keys[typ] = value
    def change(self, typ, value):
        if not isinstance(typ, (int, ActType)): return
        for i in range(len(self.keys)): # 他のキーと重複していないか
#            print('change', i, typ, self.keys[i], self.keys[typ], value)
            if typ == i: continue
#            if typ == self.keys[i]: return
            if value == self.keys[i]: return
        self.keys[typ] = value

class HomePositionKeyConfig(KeyConfig):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'HomePosition'
        self.keys[ActType.MoveL] = pyxel.KEY_S
        self.keys[ActType.MoveR] = pyxel.KEY_F
        self.keys[ActType.RollL] = pyxel.KEY_J
        self.keys[ActType.RollR] = pyxel.KEY_L
        self.keys[ActType.SpeedUp] = pyxel.KEY_D
        self.keys[ActType.Fall] = pyxel.KEY_SPACE

class KeyConfigs:
    def __init__(self):
        self.configs = [KeyConfig(), HomePositionKeyConfig(), KeyConfig()]
        self.configs[2].Name = 'User'
        self.names = KeyNames()
        self.load()
        self.now = 0
    def save(self):
        value = ''
        with open(self.FilePath, 'w') as f:
            value += str(self.now) + '\n'
            for config in self.configs:
                datas = [config.Name]
                datas.extend(map(str, config.keys))
                value += ','.join(datas) + '\n'
#            print('save', value)
            f.write(value)
    def load(self):
        if not os.path.isfile(self.FilePath): return
        self.configs.clear()
        with open(self.FilePath, 'r') as f:
            first_line = next(csv.reader(f))
            self.now = int(first_line[0])
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                config = KeyConfig()
                config.Name = row[0]
                for k in range(1, len(row)): config.set(k-1, int(row[k]))
                self.configs.append(config)
    @property
    def FilePath(self):
        here = os.path.abspath(os.path.dirname(__file__))
        parent = os.path.dirname(here)
        return os.path.join(parent, 'res', 'key.config')
    def next(self):
        if self.now < len(self.Configs) - 1:
            self.now += 1
    def previous(self):
        if 0 < self.now:
            self.now -= 1
    @property
    def Config(self): return self.configs[self.now]
    @property
    def Now(self): return self.now
    @property
    def Configs(self): return self.configs
    @property
    def Names(self): return self.names.Names

class KeyNames:
    def __init__(self):
        self.names = None
        self.load()
#        print(len(self.names))
    @property
    def FilePath(self):
        here = os.path.abspath(os.path.dirname(__file__))
        parent = os.path.dirname(here)
#        print(os.path.join(parent, 'res', 'KeyNames.txt'))
        return os.path.join(parent, 'res', 'KeyNames.txt')
    def load(self):
        if not os.path.isfile(self.FilePath): return
        with open(self.FilePath, 'r') as f:
            self.names = f.read().split('\n')
    @property
    def Names(self): return self.names

class ActNames:
    def __init__(self):
        self.names = ['Move left', 'Move Right', 'Roll left', 'Roll right', 'Speed up', 'Fall']
    @property
    def Names(self): return self.names
    

if __name__ == '__main__':
    configs = KeyConfigs()
    configs.load()
    for config in configs.Configs:
        print(config.Name, config.Keys)
        for k in config.Keys:
            print(configs.Names[k])
    configs.save()

