#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import cgi
import os
import sys
import simplejson as json
import time
from datetime import datetime

# from http://hetland.org/coding/python/levenshtein.py
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]


LANGS = {
	'russian': {
		'INTO_LATIN': {},
		'FROM_LATIN': {
			'\'': 'ь',
			'yu': 'ю',
			'ju': 'ю',
			'yo': 'ё',
			'jo': 'ё',
			'ya': 'я',
			'ja': 'я',
			'ye': 'е',
			'je': 'е',
			'a': 'а',
			'b': 'б',
			'v': 'в',
			'w': 'в',
			'g': 'г',
			'd': 'д',
			'e': 'е',
			'ż': 'ж',
			'zh': 'ж',
			'z': 'з',
			'i': 'и',
			'j': 'й',
			'k': 'к',
			'ł': 'л',
			'l': 'л',
			'm': 'м',
			'n': 'н',
			'o': 'о',
			'p': 'п',
			'r': 'р',
			's': 'с',
			't': 'т',
			'u': 'у',
			'f': 'ф',
			'h': 'х',
			'c': 'ц',
			'ch': 'ч',
			'ć': 'ч',
			'sh': 'ш',
			'sz': 'ш',
			'sch': 'щ',
			'shch': 'щ',
			'szcz': 'щ',
			'y': 'ы'
			}
		},
	'inuktitut': {
		'INTO_LATIN': {},
		'FROM_LATIN': {
			'i'	:'ᐃ',
			'ii'	:'ᐄ',
			'pi'	:'ᐱ',
			'pii'	:'ᐲ',
			'ti'	:'ᑎ',
			'tii'	:'ᑏ',
			'ki'	:'ᑭ',
			'kii'	:'ᑮ',
			'gi'	:'ᒋ',
			'gii'	:'ᒌ',
			'mi'	:'ᒥ',
			'mii'	:'ᒦ',
			'ni'	:'ᓂ',
			'nii'	:'ᓃ',
			'si'	:'ᓯ',
			'sii'	:'ᓰ',
			'li'	:'ᓕ',
			'lii'	:'ᓖ',
			'ji'	:'ᔨ',
			'jii'	:'ᔩ',
			'vi'	:'ᕕ',
			'vii'	:'ᕖ',
			'ri'	:'ᕆ',
			'rii'	:'ᕇ',
			'qi'	:'ᕿ',
			'qii'	:'ᖀ',
			'ngi'	:'ᖏ',
			'ngii'	:'ᖐ',
			'nngi'	:'ᙱ',
			'nngii'	:'ᙲ',
			'łi'	:'ᖠ',
			'łii'	:'ᖡ',

			'u'	:'ᐅ',
			'uu'	:'ᐆ',
			'pu'	:'ᐳ',
			'puu'	:'ᐴ',
			'tu'	:'ᑐ',
			'tuu'	:'ᑑ',
			'ku'	:'ᑯ',
			'kuu'	:'ᑰ',
			'gu'	:'ᒍ',
			'guu'	:'ᒎ',
			'mu'	:'ᒧ',
			'muu'	:'ᒨ',
			'nu'	:'ᓄ',
			'nuu'	:'ᓅ',
			'su'	:'ᓱ',
			'suu'	:'ᓲ',
			'lu'	:'ᓗ',
			'luu'	:'ᓘ',
			'ju'	:'ᔪ',
			'juu'	:'ᔫ',
			'vu'	:'ᕗ',
			'vuu'	:'ᕘ',
			'ru'	:'ᕈ',
			'ruu'	:'ᕉ',
			'qu'	:'ᖁ',
			'quu'	:'ᖂ',
			'ngu'	:'ᖑ',
			'nguu'	:'ᖒ',
			'nngu'	:'ᙳ',
			'nnguu'	:'ᙴ',
			'łu'	:'ᖢ',
			'łuu'	:'ᖣ',

			'a'	:'ᐊ',
			'aa'	:'ᐋ',
			'pa'	:'ᐸ',
			'paa'	:'ᐹ',
			'ta'	:'ᑕ',
			'taa'	:'ᑖ',
			'ka'	:'ᑲ',
			'kaa'	:'ᑳ',
			'ga'	:'ᒐ',
			'gaa'	:'ᒑ',
			'ma'	:'ᒪ',
			'maa'	:'ᒫ',
			'na'	:'ᓇ',
			'naa'	:'ᓈ',
			'sa'	:'ᓴ',
			'saa'	:'ᓵ',
			'la'	:'ᓚ',
			'laa'	:'ᓛ',
			'ja'	:'ᔭ',
			'jaa'	:'ᔮ',
			'va'	:'ᕙ',
			'vaa'	:'ᕚ',
			'ra'	:'ᕋ',
			'raa'	:'ᕌ',
			'qa'	:'ᖃ',
			'qaa'	:'ᖄ',
			'nga'	:'ᖓ',
			'ngaa'	:'ᖔ',
			'nnga'	:'ᙵ',
			'nngaa'	:'ᙶ',
			'ła'	:'ᖤ',
			'łaa'	:'ᖥ',

			# finals - not sure if they'll need any special handing
			'h'	:'ᐦ',
			'p'	:'ᑉ',
			't'	:'ᑦ',
			'k'	:'ᒃ',
			'g'	:'ᒡ',
			'm'	:'ᒻ',
			'n'	:'ᓐ',
			's'	:'ᔅ',
			'l'	:'ᓪ',
			'j'	:'ᔾ',
			'v'	:'ᕝ',
			'r'	:'ᕐ',
			'q'	:'ᖅ',
			'ng'	:'ᖕ',
			'nng'	:'ᖖ',
			'ł'	:'ᖦ'
			}
		}
	}


def populate_data():
	# Automagically add in a bunch of data and data structures to the LANGS
	# master list. This should run once.

	def process_list(l):
		# do some common transforms:

		# Add title-cased equivalents to convert capital characters.
		# Position of `+ l` is important since otherwise everything 
		# non-latin gets converted into title-case 
		# when title-case is first to be matched
		l = list((k.title(),v.title()) for k,v in l) + l

		# Sort by length of multi-character clumps, descending,
		# to get greedy replaces that match the longest possible string
		l.sort(key = lambda x: len(x[0]))
		l.reverse()

		return l

	for lang in LANGS:
		# Move INTO_LATIN into FROM_LATIN or vice-versa depending on 
		# which one was provided
		if len(LANGS[lang]['INTO_LATIN']) == 0:
			LANGS[lang]['INTO_LATIN'].update(dict((v,k) for k,v 
				in LANGS[lang]['FROM_LATIN'].iteritems()))
		elif len(LANGS[lang]['FROM_LATIN']) == 0:
			LANGS[lang]['FROM_LATIN'].update(dict((v,k) for k,v 
				in LANGS[lang]['INTO_LATIN'].iteritems()))

		# convert into a list to preserve a defined replace order
		LANGS[lang]['FROM_LIST'] = process_list(list((k,v) for k,v
				in LANGS[lang]['FROM_LATIN'].iteritems()))
		LANGS[lang]['INTO_LIST'] = process_list(list((k,v) for k,v
				in LANGS[lang]['INTO_LATIN'].iteritems()))

	pass

def transliterate(text, from_lang = False, to_lang = False):
	# from_lang and to_lang are not currently used. TODO: add interpreting
	# hints about source and/or destination language to aid decision-making

	# TODO: might potentially need to observe 'final only' for Inuktitut.
	# For most words, it might not be a problem thanks to greedy-matching 
	# longest possible substrings first, leaving the final alone to be 
	# matched later. But there may be some edgier cases, in which case,
	# I'll have to add a way to indicate something is a final-only symbol
	# and then do some sort of special handling (smart syllabing? might 
	# get complicated).
	# As I understand it, 'final only' can also occur at end of syllable.

	results = {}

	# For each language/substitution set, blindly try transliterating
	# input text both into and out of latin. Compute scores by evaluating
	# Levenshtein distance. Higher score == more different. 
	# If input text is already in Latin and we try transliterating into
	# Latin, result will be the same, Lev.dist == 0, and we'll disregard it
	# when evaluating the score. Ditto for e.g. transliterating Inuktitut 
	# input into Inuktitut.

	for lang in LANGS:
		into_latin = text
		from_latin = text

		for non_latin,latin in LANGS[lang]['INTO_LIST']:
			into_latin = into_latin.replace(non_latin, latin)

		for latin,non_latin in LANGS[lang]['FROM_LIST']:
			from_latin = from_latin.replace(latin, non_latin)

		scores = {
			'into': [levenshtein(into_latin, text), into_latin],
			'from': [levenshtein(from_latin, text), from_latin]
			}

		results[lang] = scores

	# Next, to find the 'correct' transliteration in the results table,
	# simply find best-scoring results (ones with largest Lev.dist. from 
	# input string) and assume they're the correct one. This mostly works,
	# though I could probably use a less-naive algorithm.

	# TODO: Some ideas to do it better:
	# - Use a ready-made language detector, particularly for inconclusive 
	#   FROM-latin cases. Ones I've seen work by recognizing known words
	#   in some database of languages' words, which might not work as well
	#   for single words.
	# - Basic detector for INTO-latin: see how many characters from the 
	#   string are in each language's INTO_LATIN collection. Language with
	#   highest amount matching wins
	# - Similarly for FROM-latin: count matching multi-character keys,
	#   e.g. 'qa' might count for Inuktitut and 'ch' for Russian.
	#   Not foolproof, but might work for two very different scripts,
	#   as I have currently.

	best_score = 0
	best_scores_data = []
	for lang in results:
		for kind in results[lang]:
			if results[lang][kind][0] > best_score:
				# if better than current best score, make it the best score
				best_score = results[lang][kind][0]
				best_scores_data = [results[lang][kind] + [lang]]
			elif best_score > 0 and results[lang][kind][0] == best_score \
				and not results[lang][kind][1] == best_scores_data[-1][1]:
				# if tied for best score, add for later deciding
				# except if it's the same result, then no point noting it again
				best_scores_data = best_scores_data + [results[lang][kind] + [lang]]

	# return either the best-scoring result or a message about a tie
	if not len(best_scores_data) == 1:
		formatted = []
		for best_score in best_scores_data:
			formatted.append(best_score[1] + ' (score ' + str(best_score[0]) 
				+ ', ' + best_score[2].title() + ')')
		return 'tie between ' + ', '.join(formatted)
	else:
		return best_scores_data[0][1]


if __name__ == '__main__':
	populate_data()

	# TODO: move these into a proper unit test, since that's what 
	# they are anyway

	print 'ᓄᓇᕗᑦ: ' + transliterate('ᓄᓇᕗᑦ')		# iqaluit
	print 'ᑰᔾᔪᐊᖅ: ' + transliterate('ᑰᔾᔪᐊᖅ')	# kuujjuaq
	print 'ᐃᖃᓗᐃᑦ: ' + transliterate('ᐃᖃᓗᐃᑦ')	# nunavut
	print 'Nunavut: ' + transliterate('Nunavut')
	print 'Yaroslav: ' + transliterate('Yaroslav')
	print 'Moskva: ' + transliterate('Moskva')
	print 'Iqaluit: ' + transliterate('Iqaluit')
	print 'Kuujjuaq: ' + transliterate('Kuujjuaq')
	print 'Владивосток: ' + transliterate('Владивосток')
	print 'Vladivostok: ' + transliterate('Vladivostok')
