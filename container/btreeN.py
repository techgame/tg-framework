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

from btree import BTree

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class BTree2(BTree):
    minDegree = 2
    maxDegree = minDegree*2 - 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree4(BTree):
    minDegree = 4
    maxDegree = minDegree*2 - 1
class BTree4x16(BTree):
    minDegree = 4
    maxDegree = 16

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree8(BTree):
    minDegree = 8
    maxDegree = minDegree*2 - 1
class BTree8x32(BTree):
    minDegree = 8
    maxDegree = 32
class BTree8x64(BTree):
    minDegree = 8
    maxDegree = 64

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree16(BTree):
    minDegree = 16
    maxDegree = minDegree*2 - 1
class BTree16x64(BTree):
    minDegree = 16
    maxDegree = 64
class BTree16x128(BTree):
    minDegree = 16
    maxDegree = 128
class BTree16x256(BTree):
    minDegree = 16
    maxDegree = 256

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree32(BTree):
    minDegree = 32
    maxDegree = minDegree*2 - 1
class BTree32x128(BTree):
    minDegree = 32
    maxDegree = 128
class BTree32x256(BTree):
    minDegree = 32
    maxDegree = 256

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree64(BTree):
    minDegree = 64
    maxDegree = minDegree*2 - 1
class BTree64x256(BTree):
    minDegree = 64
    maxDegree = 256
class BTree64x512(BTree):
    minDegree = 64
    maxDegree = 512

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree128(BTree):
    minDegree = 128
    maxDegree = minDegree*2 - 1
class BTree128x512(BTree):
    minDegree = 128
    maxDegree = 512
class BTree128x1024(BTree):
    minDegree = 128
    maxDegree = 1024

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree256(BTree):
    minDegree = 256
    maxDegree = minDegree*2 - 1
class BTree256x1024(BTree):
    minDegree = 256
    maxDegree = 1024

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTree512(BTree):
    minDegree = 512
    maxDegree = minDegree*2 - 1

