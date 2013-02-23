#!/usr/bin/env python
# coding=utf-8

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

class Transliterator(callbacks.Plugin):
	""" Supybot -> xltrtr.py interface. `tr` is the only function. """

	""" In case of problems:
	- xltrtr missing: copy or create a link to xltrtr.py in the 
	Transliterator directory (where plugin.py, __init.py__, 
	config.py also live)

	- unicode blargs in callbacks.py in irc.reply():
	older versions of supybot don't like unicode replies.
	If you don't want to update the whole package, make a change like 
	the following in $supybot/src/callbacks.py:
	https://github.com/jamessan/Supybot/commit/5bb6fdcd5202fcdeb9d4f6f1f865ff21160f1f9e
	(basically, replace
		s = str(s)
	with
		if not isinstance(s, basestring):
			# avoid trying to str() unicode
			s = str(s) # Allow non-string esses.
	"""

	def tr(self, irc, msg, args, strings):
		""" <text>
		Transliterates strings. Supports Latin transcriptions to 
		Russian Cyrillic, Latin transcriptions to Inuktitut syllabics,
		and back into Latin. Intelligently chooses which language 
		to transliterate into (please report any bugs).
		Note that only one language will be detected best matching 
		the entire <text>. """

		import xltrtr

		query = strings.decode('utf-8')
		result = xltrtr.transliterate(query)
		irc.reply(result, prefixNick = False)

	tr = wrap(tr, ['text'])

Class = Transliterator

