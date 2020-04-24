#!/usr/bin/env python3
# coding: utf8
import enum, numpy, random, pyxel
from abc import ABCMeta, abstractmethod
import keyconfig, sound

class App:
    def __init__(self):
        self.__window = Window()
        globals()['Window'] = self.__window
        self.__scene = SceneManager()
        pyxel.run(self.update, self.draw)
    def update(self):
        self.__scene.update()
    def draw(self):
        self.__scene.draw()

class Window:
    def __init__(self):
        pyxel.init(self.Width, self.Height, border_width=self.BorderWidth, caption=self.Caption, fps=60)
    @property
    def Width(self): return 120
    @property
    def Height(self): return 160
    @property
    def Caption(self): return "Tetris"
    @property
    def BorderWidth(self): return 0
    def update(self): pass
    def draw(self): pyxel.cls(0)

class SceneType(enum.IntEnum):
    Start = 0
    Config = 1
    Play  = 2
    Score = 3

class SceneManager:
    def __init__(self):
        self.__scenes = [StartScene(), ConfigScene(), PlayScene(), ScoreScene()]
        self.__now = SceneType.Start
    def init(self, *args, **kwargs):
        pass
    def update(self):
        next_scene = self.__scenes[self.__now].update()
        if isinstance(next_scene, SceneType):
            self.__now = next_scene
            self.__scenes[self.__now].init()
        elif isinstance(next_scene, tuple) and isinstance(next_scene[0], SceneType):
            self.__now = next_scene[0]
            if   2 <= len(next_scene): self.__scenes[self.__now].init(*next_scene[1])
            elif 3 <= len(next_scene): self.__scenes[self.__now].init(*next_scene[1], **next_scene[2])
            else:                      self.__scenes[self.__now].init()
    def draw(self):
        self.__scenes[self.__now].draw()

class Scene(metaclass=ABCMeta):
    @abstractmethod
    def init(self, *args, **kwargs): pass
    @abstractmethod
    def update(self): pass
    @abstractmethod
    def draw(self): pass

class StartScene(Scene):
    def __init__(self): pass
    def init(self, *args, **kwargs): pass
    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            return SceneType.Play
        if pyxel.btn(pyxel.KEY_ENTER):
            return SceneType.Config, [SceneType.Start]
    def draw(self):
        pyxel.cls(0)
        pyxel.text(Window.Width // 2 - (4*6/2), 8, 'Tetris', 7)
        pyxel.text(Window.Width // 2 - (4*14/2), Window.Height // 2 - (8*2),   'Start',  13)
        pyxel.text(Window.Width // 2 - (4* 1/2), Window.Height // 2 - (8*2),   'SPACE',  12)
        pyxel.text(Window.Width // 2 - (4*14/2), Window.Height // 2 - (8*2)+8, 'Config', 13)
        pyxel.text(Window.Width // 2 - (4* 1/2), Window.Height // 2 - (8*2)+8, 'ENTER',  12)

class ScoreScene(Scene):
    def __init__(self):
        pass
    def init(self, *args, **kwargs):
        self.__box = args[0]
    def update(self):
        if pyxel.btn(pyxel.KEY_R):
            return SceneType.Play
    def draw(self):
        self.__box.draw()
        pyxel.rect(Window.Width // 2 - (4*(10+2)//2), Window.Height // 2 - (8*(3+2)//2), (4*(10+2)), 8*(4+2), 0)
        pyxel.text(Window.Width // 2 - (4* 9/2), Window.Height // 2 - (8*2)  ,   'Game Over', 7)
        pyxel.text(Window.Width // 2 - (len(str(self.__box.Point))//2), Window.Height // 2 - (8*2)+16,   str(self.__box.Point), 10)
        pyxel.text(Window.Width // 2 - (4*10/2), Window.Height // 2 - (8*2)+32,   'Push R key', 7)

class ConfigScene(Scene):
    def __init__(self):
        self.configs = keyconfig.KeyConfigs()
        globals()['KeyConfigs'] = self.configs
        self.configs.load()
        self.actNames = keyconfig.ActNames().Names
        self.keyNames = keyconfig.KeyNames().Names
        self.line = 0
        self.ljust = max([len(s) for s in self.actNames])
        self.pause = None
    def init(self, *args, **kwargs):
        self.__pre_scene = args[0]
        if 1 < len(args): self.pause = args[1]
        self.configs.load()
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT_SHIFT) and pyxel.btn(pyxel.KEY_Q):
            if self.pause: return self.__pre_scene, [self.pause]
            else: return self.__pre_scene
        elif pyxel.btn(pyxel.KEY_LEFT_CONTROL) and pyxel.btn(pyxel.KEY_S): self.configs.save(); return;
        elif pyxel.btnp(pyxel.KEY_PAGE_UP, 60, 60): self.configs.next(); return;
        elif pyxel.btnp(pyxel.KEY_PAGE_DOWN, 60, 60): self.configs.previous(); return;
        elif not pyxel.btn(pyxel.KEY_LEFT_SHIFT) and pyxel.btnp(pyxel.KEY_UP, 10, 20):
            if 0 < self.line: self.line -= 1
        elif not pyxel.btn(pyxel.KEY_LEFT_SHIFT) and pyxel.btnp(pyxel.KEY_DOWN, 10, 20):
            if self.line < len(self.configs.Config.Keys) - 1: self.line += 1
        self.set_key()
    def set_key(self):
        key = self.get_key()
        if -1 == key: return
        self.configs.Config.change(self.line, key)
    def get_key(self):
        if pyxel.btn(pyxel.KEY_PAGE_UP): return -1
        elif pyxel.btn(pyxel.KEY_PAGE_DOWN): return -1
        elif pyxel.btn(pyxel.KEY_LEFT_SHIFT): return -1
        elif pyxel.btn(pyxel.KEY_LEFT_CONTROL): return -1
        elif pyxel.btn(pyxel.KEY_LEFT_SHIFT) and pyxel.btn(pyxel.KEY_Q): return -1
        elif pyxel.btn(pyxel.KEY_LEFT_CONTROL) and pyxel.btn(pyxel.KEY_S): return -1
        elif pyxel.btn(pyxel.KEY_LEFT_SHIFT) and pyxel.btn(pyxel.KEY_UP): return pyxel.KEY_UP
        elif pyxel.btn(pyxel.KEY_LEFT_SHIFT) and pyxel.btn(pyxel.KEY_DOWN): return pyxel.KEY_DOWN
        for key in range(len(self.keyNames)-1):
            if pyxel.btnp(pyxel.KEY_UP, 0, 30): continue
            elif pyxel.btnp(pyxel.KEY_DOWN, 0, 30): continue
            elif pyxel.btnp(pyxel.KEY_LEFT_SHIFT, 0, 30): continue
            elif pyxel.btnp(key, 0, 30): return key
        return -1
    def draw(self):
        pyxel.cls(0)
        pyxel.text(Window.Width // 2 - (4*9//2), 8*0, 'KeyConfig', 7)
        pyxel.text(0, 8*2, str(self.configs.Now) + ':' + self.configs.Config.Name, 7)
        for i, key in enumerate(self.configs.Config.Keys):
            color = 10 if i == self.line else 7
            pyxel.text(0,                  8*(i+4), self.actNames[i].ljust(self.ljust), color)
            pyxel.text(4 * (self.ljust+1), 8*(i+4), self.configs.Names[key], color)
        pyxel.text(0,       8*len(self.configs.Config.Keys)+24+16, 'Quit', 13)
        pyxel.text(4*(7+1), 8*len(self.configs.Config.Keys)+24+16, 'SHIFT+Q', 12)
        pyxel.text(0,       8*len(self.configs.Config.Keys)+24+24, 'Save', 13)
        pyxel.text(4*(7+1), 8*len(self.configs.Config.Keys)+24+24, 'CTRL+S', 12)
        pyxel.text(0,       8*len(self.configs.Config.Keys)+24+32, 'Move', 13)
        pyxel.text(4*(7+1), 8*len(self.configs.Config.Keys)+24+32, 'Up,Down', 12)
        pyxel.text(0,       8*len(self.configs.Config.Keys)+24+40, 'Select', 13)
        pyxel.text(4*(7+1), 8*len(self.configs.Config.Keys)+24+40, 'PgUp,PgDown', 12)

class PlayScene(Scene):
    def __init__(self):
        self.init()
    def init(self, *args, **kwargs):
        if args and 0 < len(args): self.__box = args[0]
        else: self.__box = Box()
    def update(self):
        if self.__box.is_gameover():
            return SceneType.Score, [self.__box]
        if pyxel.btn(pyxel.KEY_LEFT_SHIFT) and pyxel.btn(pyxel.KEY_C):
            return SceneType.Config, [SceneType.Play, self.__box]
        else: self.__box.update()
    def draw(self):
        self.__box.draw()

class Box:
    WIDTH = 10
    HEIGHT = 20
    def __init__(self):
        self.__point = 0
        self.__blocks = numpy.zeros((Box.WIDTH * Box.HEIGHT)).reshape(Box.HEIGHT, Box.WIDTH)
        self.__gen = TetriminoGenerator()
        self.__mino = self.__gen.generate()
        self.__estimate_y = 0
        self.__point = 0
        self.__sound = sound.Sound()
    def update(self):
        if 0 == pyxel.frame_count % 30:
            self.__mino.y += 1
        if pyxel.btnp(pyxel.KEY_F3, 0, 50): self.__sound.toggle_mute()
        if pyxel.btnp(KeyConfigs.Config.Keys[keyconfig.ActType.SpeedUp], 10, 10):
            if self.__detect_collision(): return
            self.__mino.y += 1
        if pyxel.btnp(KeyConfigs.Config.Keys[keyconfig.ActType.Fall], 0, 50):
            if self.__detect_collision(): return
            self.__mino.y = self.__estimate_y
        if pyxel.btnp(KeyConfigs.Config.Keys[keyconfig.ActType.RollL], 0, 30): self.__mino.rollL(); self.__sound.decrement_key()
        if pyxel.btnp(KeyConfigs.Config.Keys[keyconfig.ActType.RollR], 0, 30): self.__mino.rollR(); self.__sound.increment_key()
        if pyxel.btnp(KeyConfigs.Config.Keys[keyconfig.ActType.MoveL], 10, 5):
            self.__mino.moveL(self.__blocks)
        if pyxel.btnp(KeyConfigs.Config.Keys[keyconfig.ActType.MoveR], 10, 5):
            self.__mino.moveR(self.__blocks)
        self.__estimate_detect_collision()
        self.stack()
        self.vanish()
    def is_gameover(self):
        for x in range(Box.WIDTH):
            if 0 != self.__blocks[0][x]: return True
        return False
    def stack(self): # 落下ブロックの確定（積み上げ）
        if not self.__detect_collision(): return
#        print('stack!', self.__mino.x, self.__mino.y)
        for i in range(len(self.__mino.blocks)):
            if 0 == self.__mino.blocks[i]: continue
            x = self.__mino.x + (i%4)
            y = self.__mino.y + (i//4)
            if Box.HEIGHT - 1 < y: continue
            if Box.WIDTH - 1 < x: continue
            self.__blocks[y][x] = self.__mino.blocks[i]
#            print(x, y, self.__blocks[y][x])

        self.__sound.sound(self.__gen.MinoId)
        self.__mino = self.__gen.generate()
    def __detect_collision(self):
        for i in range(len(self.__mino.blocks)):
            if 0 == self.__mino.blocks[i]: continue
            by = i // 4
            bx = i % 4
            x = self.__mino.x + bx
            y = self.__mino.y + by
            if Box.WIDTH - 1 < x: continue
            if Box.HEIGHT <= y:
                self.__mino.y -= 1
                y -= 1
#                print('detect! A', x, y, self.__mino.y)
                return True
            if 0 != self.__blocks[y][x]:
                self.__mino.y -= 1
                y -= 1
#                print('detect! B', x, y, self.__mino.y)
                return True
        return False

    def vanish(self): # 消滅
        for y in range(Box.HEIGHT):
            count = 0
            for x in range(Box.WIDTH):
                if 0 != self.__blocks[y][x]: count += 1
            if count == Box.WIDTH:
                for x in range(Box.WIDTH):
                    self.__blocks[y][x] = 0
#                print('vanish!', y)
                self.__down_alignment(y)
                self.__point += 1
    def __down_alignment(self, vy): # 下に詰める
        for y in reversed(range(vy)):
            for x in range(Box.WIDTH):
                self.__blocks[y+1][x] = self.__blocks[y][x]

    def __estimate_detect_collision(self): # 落下予測位置の算出
        for estimate_y in range(self.__mino.y, Box.HEIGHT):
            for i in range(len(self.__mino.blocks)):
                if 0 == self.__mino.blocks[i]: continue
                by = i // 4
                bx = i % 4
                x = self.__mino.x + bx
                y = estimate_y + by
#                print('estimate', y, estimate_y)
                if Box.WIDTH - 1 < x: continue
                if Box.HEIGHT - 1 < y: continue
                if 0 != self.__blocks[y][x]: # 下端より上
                    estimate_y -= 1
                    y -= 1
                    self.__estimate_y = estimate_y
#                    print('estimate detect! A', x, y, self.__estimate_y)
                    return estimate_y
                else: # 下端
                    max = by
                    for c in range(y+1, len(self.__mino.blocks)):
                        candidate = c // 4
                        if candidate < max: max = candidate
                    if y + self.__mino.h <= Box.HEIGHT - 1:
                        self.__estimate_y = y

    def draw(self):
        pyxel.cls(13)
        self.draw_blocks()
        self.draw_fall()
        self.draw_grid()
        self.draw_next()
        self.draw_point()
        self.draw_key()
    def draw_blocks(self):
        for y in range(Box.HEIGHT):
            for x in range(Box.WIDTH):
                color = 7 if 0 == self.__blocks[y][x] else self.__blocks[y][x]
                pyxel.rect(Block.Size*x, Block.Size*y, Block.Size, Block.Size, color)
    def draw_fall(self): # 落下中テトリミノ
        for i in range(len(self.__mino.blocks)):
            by = i // 4
            bx = i % 4
            x = self.__mino.x + bx
            y = self.__mino.y + by
            if 0 == self.__mino.blocks[i]: continue
            pyxel.rect(Block.Size*x, (Block.Size*(by+self.__estimate_y)), Block.Size, Block.Size, 14) # 衝突予測テトリミノ
            pyxel.rect(Block.Size*x, Block.Size*y, Block.Size, Block.Size, self.__mino.blocks[i]) # 落下中テトリミノ
    def draw_grid(self):
        for y in range(Box.HEIGHT):
            pyxel.line(0, Block.Size*y, Block.Size*Box.WIDTH, Block.Size*y, 12)
        for x in range(Box.WIDTH):
            pyxel.line(Block.Size*x, 0, Block.Size*x, Block.Size*Box.HEIGHT, 12)
    def draw_next(self):
        for m, mino in enumerate(self.__gen.Nexts):
            for i in range(len(mino.blocks)):
                if 0 == mino.blocks[i]: continue
                y = i // 4 + (4 * m)
                x = i % 4
                pyxel.rect((Block.Size*x)+((Box.WIDTH)*Block.Size)+Block.Size//2, Block.Size*y, Block.Size, Block.Size, mino.blocks[i])
    def draw_point(self):
        s = str(self.__point)
        pyxel.text(Window.Width - len(s)*4, Window.Height - Block.Size, s, 8)
    def draw_key(self):
        s = 'SHIFT+C'
        pyxel.text(Window.Width - len(s)*4, Window.Height - Block.Size*3, s, 7)
        s = 'F3'
        if self.__sound.IsMute: s += ' :Mute'
        pyxel.text(Window.Width - len(s)*4, Window.Height - Block.Size*4, s, 7)
     
    @property
    def Point(self): return self.__point

class Block:
    Size = 8

class TetriminoRandomGenerator:
    def __init__(self):
        self.__minos = (TetriminoI(), TetriminoO(), TetriminoS(), TetriminoZ(), TetriminoJ(), TetriminoL(), TetriminoT())
    def generate(self):
        return self.__minos[random.randint(0, len(self.__minos))]

# 落下テトリミノ。法則あり。7種類が必ず1個ずつ落ちる。その順序がランダム。
class TetriminoOfficalGenerator:
    def __init__(self):
        self.__minos = (TetriminoI, TetriminoO, TetriminoS, TetriminoZ, TetriminoJ, TetriminoL, TetriminoT)
        self.__order = random.sample(list(range(len(self.__minos))), len(self.__minos))
        self.__order_count = -1
    def generate(self):
        if len(self.__minos) - 1 <= self.__order_count:
            random.shuffle(self.__order)
            self.__order_count = 0
        else: self.__order_count += 1
        mino = self.__minos[self.__order[self.__order_count]]()
        mino.init()
        return mino
    @property
    def MinoId(self): return self.__order[self.__order_count]

# 落下テトリミノ。次回ミノを参照できる
class TetriminoGenerator:
    def __init__(self):
        self.__generator = TetriminoOfficalGenerator()
        self.__nexts = []
        for i in range(4): self.__nexts.append(self.__generator.generate())
    def generate(self):
        now = self.__nexts.pop(0)
        self.__nexts.append(self.__generator.generate())
        return now
    @property
    def Nexts(self): return self.__nexts[:3]
    @property
    def MinoId(self): return self.__generator.MinoId

class Tetrimino:
    def __init__(self):
        self.blocks = [0,0,0,0,
                       0,0,0,0,
                       0,0,0,0,
                       0,0,0,0]
        self.color = 0
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.__diffR = (3,6,9,12,-2,1,4,7,-7,-4,-1,2,-12,-9,-6,-3)
        self.__diffL = (12,7,2,-3,9,4,-1,-6,6,1,-4,-9,3,-2,-7,-12)
    def init(self):
        self.__get_width()
        self.__get_height()
        self.x = (Box.WIDTH // 2) - 1
    def moveL(self, blocks):
        for i in range(len(self.blocks)):
            if 0 == self.blocks[i]: continue
            x = i % 4
            y = i // 4
            left = self.x + x - 1
            if left < 0: continue
            elif 0 != blocks[self.y+y][left]: return
        if 0 < self.x: self.x -= 1
    def moveR(self, blocks):
        for i in range(len(self.blocks)):
            if 0 == self.blocks[i]: continue
            x = i % 4
            y = i // 4
            if Box.HEIGHT - 1 < self.y+y: continue
            right = self.x + x + 1
            if Box.WIDTH - 1 < right: continue
            elif 0 != blocks[self.y+y][right]: return
        if self.x + self.__get_width() < Box.WIDTH - 1:
            self.x += 1
    def __get_width(self):
        max = 0
        for i in range(len(self.blocks)):
            if 0 == self.blocks[i]: continue
            x = i % 4
            if max < x: max = x
        self.w = max
        return max
    def __get_height(self):
        max = 0
        for i in range(len(self.blocks)):
            if 0 == self.blocks[i]: continue
            y = i // 4
            if max < y: max = y
        self.h = max
        return max

    def rollR(self): self.__roll(self.__diffR); self.__in_bound();
    def rollL(self): self.__roll(self.__diffL); self.__in_bound();
    def __roll(self, diffs):
        new = list(self.blocks)
        for i in range(len(self.blocks)):
            new[i+diffs[i]] = self.blocks[i]
        self.blocks = new
        self.__roll_left_alignment()
        self.__get_width()
        self.__get_height()
    def __roll_left_alignment(self): # 左寄せする
        for r in range(4):
            if self.__is_left_alignment(): break
            new = numpy.zeros(len(self.blocks)).tolist()
            for i in range(len(self.blocks)):
                if 3 == i % 4: new[i] = 0
                else: new[i] = self.blocks[i+1]
            self.blocks = new
    def __is_left_alignment(self): # 左寄せされているか
        for i in (0,4,8,12):
            if 0 != self.blocks[i]: return True
        return False
    def __in_bound(self): # 回転して枠外にはみ出たら枠内に戻す
        w = self.__get_width()
        if Box.WIDTH - 1 < self.x + w:
            self.x -= (self.x + w) - (Box.WIDTH - 1)
#            print('__in_bound')

class TetriminoI(Tetrimino):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.blocks = [6,6,6,6,
                       0,0,0,0,
                       0,0,0,0,
                       0,0,0,0]
        self.color = 6
class TetriminoO(Tetrimino):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.blocks = [10,10,0,0,
                       10,10,0,0,
                        0, 0,0,0,
                        0, 0,0,0]
        self.color = 10
class TetriminoS(Tetrimino):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.blocks = [ 0,11,11,0,
                       11,11, 0,0,
                        0, 0, 0,0,
                        0, 0, 0,0]
        self.color = 11
class TetriminoZ(Tetrimino):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.blocks = [8,8,0,0,
                       0,8,8,0,
                       0,0,0,0,
                       0,0,0,0]
        self.color = 8
class TetriminoJ(Tetrimino):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.blocks = [5,0,0,0,
                       5,5,5,0,
                       0,0,0,0,
                       0,0,0,0]
        self.color = 5
class TetriminoL(Tetrimino):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.blocks = [0,0,9,0,
                       9,9,9,0,
                       0,0,0,0,
                       0,0,0,0]
        self.color = 9
class TetriminoT(Tetrimino):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.blocks = [0,2,0,0,
                       2,2,2,0,
                       0,0,0,0,
                       0,0,0,0]
        self.color = 2


App()
