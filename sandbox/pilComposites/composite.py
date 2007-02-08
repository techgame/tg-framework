#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import time
from PIL import Image
from TG.common.path import path

from TG.guiTools.pil import layers
from TG.guiTools.pil import blending
#from TG.guiTools.pil import strategies

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Combo(object):
    def __init__(self, size=None):
        self.load(size)

    def load(self, size=None):
        if size is None: 
            resize = lambda img: img
        else:
            resize = lambda img: img.resize(size, Image.ANTIALIAS)
            #resize = lambda img: img.resize(size, Image.BILINEAR)
        self.shadow = resize(Image.open('shadow.png'))
        self.base = resize(Image.open('base.png'))
        self.logo = resize(Image.open('logo.png'))
        self.reflection = resize(Image.open('reflection.png'))

    def layerDodge(self, color):
        def composition():
            def topGroup():
                yield layers.ImageLayer(self.reflection, blend='blend(0.15)')
                yield layers.ColorLayer((0,0,0,255))
            yield topGroup()

            def ballGroup():
                colorLayer = layers.ColorLayer(color)
                logo = layers.ImageLayer(self.logo, blend='colordodge')
                yield (logo, colorLayer)
                base = layers.ImageLayer(self.base, blend='multiply')
                yield (base, colorLayer)

            yield ballGroup()
            yield layers.ImageLayer(self.shadow)

        comp = layers.GroupLayer(composition())
        return comp.getImage()

    def layerMultiply(self, color):
        def composition():
            yield layers.ImageLayer(self.reflection)
            def ballGroup():
                colorLayer = layers.ColorLayer(color)
                logo = layers.ImageLayer(self.logo, blend='multiply')
                yield (logo, colorLayer)
                base = layers.ImageLayer(self.base, blend='multiply')
                yield (base, colorLayer)

            yield ballGroup()

            yield layers.ImageLayer(self.shadow)

        comp = layers.GroupLayer(composition())
        return comp.getImage()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    t = 0.0
    l = Combo((100,100))
    #l = Combo(None)

    if os.path.isdir('comparisons'):
        os.system('rm -rf comparisons/*')
    else:
        os.mkdir('comparisons')
    #os.chdir('comparisons')

    out = open('comparisons/imgs.html', 'w')
    print >> out, '<html>'
    print >> out, '    <body bgcolor="%s">' % ('#aaaaaa',)

    for c in [
            (255,0,0,255),
            (0, 255,0,255),
            (0,0,255,255),
            (255,0,255,255),
            (252, 189, 3, 255),
            ]:

        for methodName, method in (
                ('mult', l.layerMultiply), 
                ('dodge', l.layerDodge),
                ):
            filename = methodName + '-{%s,%s,%s,%s}.png' % c
            print filename

            s = time.clock()
            img = method(c)
            t += time.clock() - s
            img.save('comparisons/' + filename)
            print >> out, '        <img src="%s" />' % filename
        print

    print >> out, '    </body>'
    print >> out, '</html>'
    print t

if __name__=='__main__':
    main()

