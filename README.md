[ja](./README.ja.md)

# Pyxel.Tetris

Tetris (made by Pyxel)

# DEMO

![demo_all](doc/demo_all.gif)
![demo_play](doc/demo_play.gif)
![demo_config](doc/demo_config.gif)

# Requirement

* <time datetime="2020-04-14T18:13:05+0900">2020-04-14</time>
* [Raspbierry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 4 Model B Rev 1.2
* [Raspbian](https://ja.wikipedia.org/wiki/Raspbian) buster 10.0 2019-09-26 <small>[setup](http://ytyaru.hatenablog.com/entry/2019/12/25/222222)</small>
* bash 5.0.3(1)-release
* Python 3.7.3
* [pyxel][] 1.3.1

[pyxel]:https://github.com/kitao/pyxel

```sh
$ uname -a
Linux raspberrypi 4.19.97-v7l+ #1294 SMP Thu Jan 30 13:21:14 GMT 2020 armv7l GNU/Linux
```

# Installation

Install Python 3.7 or higher.

Next, install [pyxel][] as follows.

* [pyxel/README](https://github.com/kitao/pyxel/blob/master/README.md#how-to-install)

```sh
sudo apt install python3 python3-pip libsdl2-dev libsdl2-image-dev
git clone https://github.com/kitao/pyxel.git
cd pyxel
make -C pyxel/core clean all
pip3 install .
```

# Usage

```sh
git clone https://github.com/ytyaru/Python.Pyxel.Tetris.20200424000000
cd Python.Pyxel.Tetris.20200424000000/src
./run.sh
```

## Start

Meaning|key
-------|---
Start playing|`SPACE`
Key config|`Enter`

![start](demo/start.png)

## KeyConfig

![keyconfig](demo/keyconfig.png)

Meaning|key
----|----
Back|`Shift`+`Q`
Save|`Ctrl`+`S`
Move cursor|`↑`, `↓`
Selection decision|`PgUp`,` PgDn`

* Key config can save up to 3 settings. Select and use one of them.

Change the key as follows.

1. Move the cursor to the item you want to change
2. Press the key you want to set

No duplicate keys allowed. If you want to set the already set key to another item, specify another key once.

### Default setting

`0: Default` is selected.

item|0:Default|1:HomePosition|2:User
----|---------|--------------|------
Move left|`←`|`S`|`S`
Move right|`→`|`F`|`D`
Roll left|`L`|`J`|`A`
Roll right|`R`|`L`|`F`
Speed up|`↓`|`D`|`G`
Fall|`Space`|`Space`|`Space`

## Play

Meaning|key
-------|----
Key config|`Shift`+`C`
Mute switch|`F3`

* Operate using the key set / selected on the key configuration screen
* You can call the key config screen by suspending with `Shift` +` C`

![play](demo/play.png)
![mute](demo/mute.png)

## GameOver

* The number of deleted lines is displayed
* You can retry by pressing the `R` key

![gameover](demo/gameover.png)

# Note

* Bug. Fall Prediction Tetrimino sometimes slips below the bottom edge
* There is a sound. When I put Tetrimino. There is no mute setting

# Author

ytyaru

* [![github](http://www.google.com/s2/favicons?domain=github.com)](https://github.com/ytyaru "github")
* [![hatena](http://www.google.com/s2/favicons?domain=www.hatena.ne.jp)](http://ytyaru.hatenablog.com/ytyaru "hatena")
* [![mastodon](http://www.google.com/s2/favicons?domain=mstdn.jp)](https://mstdn.jp/web/accounts/233143 "mastdon")

# License

This software is CC0 licensed.

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.en)

