#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import cgi
import os
import sys
import simplejson as json

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
        'INTO_LATIN': {
            'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'g',
            'д': 'd',
            'е': 'ye',
            'ё': 'yo',
            'ж': 'zh',
            'з': 'z',
            'и': 'i',
            'й': 'j',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'kh',
            'ц': 'c',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'shch',
            'ъ': 'ʺ',
            'ы': 'y',
            'ь': '\'',
            'э': 'e',
            'ю': 'yu',
            'я': 'ya'
            },
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
            'i' :'ᐃ',
            'ii'    :'ᐄ',
            'pi'    :'ᐱ',
            'pii'   :'ᐲ',
            'ti'    :'ᑎ',
            'tii'   :'ᑏ',
            'ki'    :'ᑭ',
            'kii'   :'ᑮ',
            'gi'    :'ᒋ',
            'gii'   :'ᒌ',
            'mi'    :'ᒥ',
            'mii'   :'ᒦ',
            'ni'    :'ᓂ',
            'nii'   :'ᓃ',
            'si'    :'ᓯ',
            'sii'   :'ᓰ',
            'li'    :'ᓕ',
            'lii'   :'ᓖ',
            'ji'    :'ᔨ',
            'jii'   :'ᔩ',
            'vi'    :'ᕕ',
            'vii'   :'ᕖ',
            'ri'    :'ᕆ',
            'rii'   :'ᕇ',
            'qi'    :'ᕿ',
            'qii'   :'ᖀ',
            'ngi'   :'ᖏ',
            'ngii'  :'ᖐ',
            'nngi'  :'ᙱ',
            'nngii' :'ᙲ',
            'łi'    :'ᖠ',
            'łii'   :'ᖡ',

            'u' :'ᐅ',
            'uu'    :'ᐆ',
            'pu'    :'ᐳ',
            'puu'   :'ᐴ',
            'tu'    :'ᑐ',
            'tuu'   :'ᑑ',
            'ku'    :'ᑯ',
            'kuu'   :'ᑰ',
            'gu'    :'ᒍ',
            'guu'   :'ᒎ',
            'mu'    :'ᒧ',
            'muu'   :'ᒨ',
            'nu'    :'ᓄ',
            'nuu'   :'ᓅ',
            'su'    :'ᓱ',
            'suu'   :'ᓲ',
            'lu'    :'ᓗ',
            'luu'   :'ᓘ',
            'ju'    :'ᔪ',
            'juu'   :'ᔫ',
            'vu'    :'ᕗ',
            'vuu'   :'ᕘ',
            'ru'    :'ᕈ',
            'ruu'   :'ᕉ',
            'qu'    :'ᖁ',
            'quu'   :'ᖂ',
            'ngu'   :'ᖑ',
            'nguu'  :'ᖒ',
            'nngu'  :'ᙳ',
            'nnguu' :'ᙴ',
            'łu'    :'ᖢ',
            'łuu'   :'ᖣ',

            'a' :'ᐊ',
            'aa'    :'ᐋ',
            'pa'    :'ᐸ',
            'paa'   :'ᐹ',
            'ta'    :'ᑕ',
            'taa'   :'ᑖ',
            'ka'    :'ᑲ',
            'kaa'   :'ᑳ',
            'ga'    :'ᒐ',
            'gaa'   :'ᒑ',
            'ma'    :'ᒪ',
            'maa'   :'ᒫ',
            'na'    :'ᓇ',
            'naa'   :'ᓈ',
            'sa'    :'ᓴ',
            'saa'   :'ᓵ',
            'la'    :'ᓚ',
            'laa'   :'ᓛ',
            'ja'    :'ᔭ',
            'jaa'   :'ᔮ',
            'va'    :'ᕙ',
            'vaa'   :'ᕚ',
            'ra'    :'ᕋ',
            'raa'   :'ᕌ',
            'qa'    :'ᖃ',
            'qaa'   :'ᖄ',
            'nga'   :'ᖓ',
            'ngaa'  :'ᖔ',
            'nnga'  :'ᙵ',
            'nngaa' :'ᙶ',
            'ła'    :'ᖤ',
            'łaa'   :'ᖥ',

            # finals - not sure if they'll need any special handing
            'h' :'ᐦ',
            'p' :'ᑉ',
            't' :'ᑦ',
            'k' :'ᒃ',
            'g' :'ᒡ',
            'm' :'ᒻ',
            'n' :'ᓐ',
            's' :'ᔅ',
            'l' :'ᓪ',
            'j' :'ᔾ',
            'v' :'ᕝ',
            'r' :'ᕐ',
            'q' :'ᖅ',
            'ng'    :'ᖕ',
            'nng'   :'ᖖ',
            'ł' :'ᖦ'
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
                in LANGS[lang]['FROM_LATIN'].items()))
        elif len(LANGS[lang]['FROM_LATIN']) == 0:
            LANGS[lang]['FROM_LATIN'].update(dict((v,k) for k,v 
                in LANGS[lang]['INTO_LATIN'].items()))

        # convert into a list to preserve a defined replace order
        LANGS[lang]['FROM_LIST'] = process_list(list((k,v) for k,v
                in LANGS[lang]['FROM_LATIN'].items()))
        LANGS[lang]['INTO_LIST'] = process_list(list((k,v) for k,v
                in LANGS[lang]['INTO_LATIN'].items()))

    pass

def find_best_score(l):
    # Takes a list containing dicts composed as follows:
    #   {score, output, ... possible further information}
    # and returns a list with only those items that have the highest score
    # of all items. If there's only one highest score, result is a list 
    # of one item; otherwise, all the highest-score items are in the list.

    best_score = 0
    best_scores_data = []
    for entry in l:
        if entry['score'] > best_score:
            # if better than current best score, make it the best score
            best_score = entry['score']
            best_scores_data = [entry]
        elif best_score > 0 and entry['score'] == best_score \
            and not entry['output'] == best_scores_data[-1]['output']:
            # if tied for best score, add for later deciding
            # except if it's the same result, then no point noting it again

            # TODO: technically we can still get duplicate results
            # if there are other results in between them 
            # (because we only check index -1, the last item).
            # If this becomes a problem, look more thoroughly.
            best_scores_data = best_scores_data + [entry]
    
    return best_scores_data

def transliterate(text, from_lang = False, to_lang = False):
    # from_lang and to_lang are not currently used. TODO: add interpreting
    # hints about source and/or destination language to aid decision-making

    # TODO: might potentially need to observe 'final only' for Inuktitut.
    # For most words, it might not be a problem thanks to greedy-matching 
    # longest possible substrings first, leaving the final alone to be 
    # matched later. But there may be some edgier cases, in which case,
    # I'll have to add a way to indicate something is a final-only symbol
    # and then do some sort of special handling.
    # As I understand it, 'final only' can also occur at end of syllable.
    # So smart syllabing? Might get complicated.

    # For each language/substitution set, first blindly try transliterating
    # input text both into and out of latin. Compute scores by evaluating
    # Levenshtein distance. Higher score == more different. 
    # If input text is already in Latin and we try transliterating into
    # Latin, result will be the same, and Lev.dist score == 0.
    # Ditto for e.g. transliterating Inuktitut input into Inuktitut.

    # Next, count matching language keys in the source string. 
    # E.g. 'ch' might count for Russian and 'qa' for Inuktitut.
    # Scores are weighted by length, as a match for 'shch' or 'kuu' 
    # is much more indicative than a match for 'a'.

    # Finally, results where not every character has been replaced receive 
    # penalty points. For transliterating "iqaluit" from Latin script,
        # ᐃᖃᓗᐃᑦ is an obviously better result than иqалуит, 
    # since the Latin "q" isn't part of Russian Cyrillic script.
    # Technically, this is done by checking how many of the characters in 
    # the produced output are transliterable back. For the example, 
    # all of ᐃᖃᓗᐃᑦ converts back into Latin, while the q in "иqалуит"
    # would not be touched by a Russian to Latin transliteration.

    # Not foolproof, but again, mostly works, particularly for two 
    # very different scripts, as I have currently.

    # TODO: Some more ideas to do it better:
    # - Use a ready-made language detector, particularly for inconclusive 
    #   FROM-latin cases. Ones I've seen work by recognizing known words
    #   in some database of languages' words, which might not work as well
    #   for single words.

    scores = []

    def score(text, lang, direction):
        # score transliteration in desired direction w.r.t. Latin script
        # ('into' => "into Latin script", otherwise "from Latin script")

        transliterated = text

        direction = direction.upper()
        opposite_direction = 'FROM' if (direction == 'INTO') else 'INTO'
        direction_list = direction + '_LIST'
        opposite_direction_list = opposite_direction + '_LIST'

        # first, transliterate, and check its Levenshein score
        # - weigh by length of input
        for find,replace in LANGS[lang][direction_list]:
            transliterated = transliterated.replace(find, replace)
        lev_score = levenshtein(transliterated, text) * len(text)

        # give points for each character matched
        # - add extra weight for longer clumps
        clump_score = 0
        for clump,ignore in LANGS[lang][direction_list]:
            match = clump.lower()
            clump_score += text.count(match) * len(match)

        # see how much was NOT matched, and take away points
        # - weight by length of output, as longer outputs will tend to have 
        # otherwise higher scores
        # - strip down reverse_test_string gradually as we find matches
        # to avoid double or triple counting matches in combinations 
        # like "kii" (would otherwise match for "i", "ki", and "kii") or "ya"
        reverse_score = 0
        reverse_test_string = transliterated
        for clump,ignore in LANGS[lang][opposite_direction_list]:
            reverse_score += reverse_test_string.count(clump) * len(clump)
            reverse_test_string = reverse_test_string.replace(clump, '')
        # compare number of matches against length of output string to see
        # if we missed something
        reverse_score = -1 * abs(len(transliterated) - reverse_score) \
            * len(transliterated)

        return {'output': transliterated, 
            'lev': lev_score, 'clump': clump_score, 'penalty': reverse_score}

    for lang in LANGS:
        # score transliteration from other script into Latin script
        INTO = score(text, lang, 'into')

        scores.append({
            'score': (INTO['lev'] + INTO['clump'] + INTO['penalty']), 
            'scores': {'lev': INTO['lev'], 'clump': INTO['clump'], 
                'penalty': INTO['penalty']}, 
            'lang': lang, 'dir': 'into', 'output': INTO['output']});

        # score transliteration from Latin into other script
        FROM = score(text, lang, 'from')

        scores.append({
            'score': (FROM['lev'] + FROM['clump'] + FROM['penalty']), 
            'scores': {'lev': FROM['lev'], 'clump': FROM['clump'], 
                'penalty': FROM['penalty']}, 
            'lang': lang, 'dir': 'from', 'output': FROM['output']});

    scores.sort(key = lambda x: x['score'], reverse = True)

    return scores

def format_text(data):
    # return either the best-scoring result or a string message about a tie
    data = find_best_score(data)
    if not len(data) == 1:
        formatted = []
        for best_score in data:
            formatted.append(best_score['output'] + \
                ' (' + best_score['lang'].title() + ')')
        return 'tie between ' + ', '.join(formatted)
    else:
        return data[0]['output']

#__init__
# except this isn't a class...
populate_data()

if __name__ == '__main__':
    # check if we're running as CGI
    # this uses RFC3875 section 4.1.4
    isCGI = 'GATEWAY_INTERFACE' in os.environ

    if isCGI:
        # cgi.FieldStorage() *really* doesn't like being called before
        # something is printed, at least in python 2.6.6 on my webhost.
        # So print the Content-Type header.
        # Do no print newline so that the content-type can be changed
        # by printing a second header later. This is used to send HTML
        # from this same file.
        print 'Content-Type: application/json'

        args = cgi.FieldStorage()

        if 'query' in args and 'ajax' in args:
            print '\n' # newline to signal end of header field

            # print JSON output with all data
            # (scores for all combinations, sorted descending)
            xl = transliterate(args['query'].value.decode('utf-8'))
            print json.dumps(xl)
        else:
            print 'Content-Type: text/html\n' # we'll be sending HTML instead

            # TODO: if 'query' in args, compute transliteration and inject into
            # printed HTML so it'll work on browsers with disabled js or xhr
            f = open('frontend.html', 'r')
            html = f.read()
            print html

     # if we aren't CGI, assume command-line behaviour
    else:
        args = []

        if len(sys.argv) > 1:
            source = u' '.join(arg.decode('utf-8') for arg in sys.argv[1:])
            print '%s: %s' % (source, format_text(transliterate(source)))

        else:
            print './xltrtr.py [string]'
            print '\ttransliterate string into best-guess of either Inuktitut or Russian'

