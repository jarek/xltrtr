#!/usr/bin/env python
# coding=utf-8

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Transliterator', True)

Climate = conf.registerPlugin('Transliterator')

