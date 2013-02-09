#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import unittest
import xltrtr

class known_values(unittest.TestCase):
	basic_values = (
		('ᓄᓇᕗᑦ', 'nunavut'),
		('ᑰᔾᔪᐊᖅ', 'kuujjuaq'),
		('ᐃᖃᓗᐃᑦ', 'iqaluit'),
		('ᐅᐃᑭᐱᑎᐊ', 'uikipitia'),
		('ᔪᐊᑕᓐ ᑐᑐ', 'juatan tutu'),
		#('ᓄᖅᑲᕆᑦ', 'nuqqarit'), # wikipedia says this should be nuqqarit - from what i can see it might be nuqkarit or inuktitut might be written down wrong - verify
		('ᓯᑮᑐ', 'sikiitu'), # ski-doo :D
		('ᐃᓄᒃᑕᐅᑦ', 'inuktaut'), # bus

		('Iqaluit', 'ᐃᖃᓗᐃᑦ'),
		('Nunavut', 'ᓄᓇᕗᑦ'),
		('Kuujjuaq', 'ᑰᔾᔪᐊᖅ'),
	
		('Ярослав', 'Yaroslav'),
		('Владивосток', 'Vladivostok'),

		('Moskva', 'Москва'),
		('Vladivostok', 'Владивосток'),
		('Władiwostok', 'Владивосток'),

		)

	sanity_values = (
		'ᓄᓇᕗᑦ',
		'ᑰᔾᔪᐊᖅ',
		'ᐃᖃᓗᐃᑦ',
		'ᐅᐃᑭᐱᑎᐊ',
		'ᔪᐊᑕᓐ ᑐᑐ',
		'ᓄᖅᑲᕆᑦ',

		'iqaluit',
		'nunavut',
		'kuujjuaq',
	
		'Vladivostok',
		# currently script only works from Russian,
		# not Polish-flavoured Cyrillic
		#'Władiwostok',
		'Yaroslav',
		'Moskva',
		'moskva',
		)		
	
	def test_basic_case(self):
		"""transliterate() should give known result with known input"""

		for source, to in self.basic_values:
			#print '%s = %s' % (source, to)
			result = xltrtr.transliterate(source)
			self.assertEqual(to, result)
	
	def test_sanity_case(self):
		"""transliterate() should give consistent results for round-trip transliterations"""

		for source in self.sanity_values:
			intermediate = xltrtr.transliterate(source)
			result = xltrtr.transliterate(intermediate)

			#print '%s = %s = %s' % (source, intermediate, result)
			self.assertEqual(source, result)

if __name__ == '__main__':
	unittest.main()
