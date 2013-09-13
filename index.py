#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import cgi
import os
import simplejson as json
import xltrtr


def find_template(html, template_name):
    template_tag = '<script type="text/template" id="' + template_name + '">'
    template_close_tag = '</script>'
    index1 = html.find(template_tag)
    index2 = html.find(template_close_tag, index1)
    return html[index1+len(template_tag):index2]

if __name__ == '__main__':
    # check if we're running as CGI
    # this uses RFC3875 section 4.1.4
    isCGI = 'GATEWAY_INTERFACE' in os.environ

    if isCGI:
        # cgi.FieldStorage() *really* doesn't like being called before
        # something is printed, at least in python 2.6.6 on my webhost.
        # So print the Content-Type header.
        # Do not print newline, so that the content-type can be changed
        # by printing a second header later. This is used to send HTML
        # from this same file.
        print 'Content-Type: application/json'

        args = cgi.FieldStorage()

        if 'query' in args and 'ajax' in args:
            print '\n' # newline to signal end of header field

            # print JSON output with all data
            # (scores for all combinations, sorted descending)
            query = args['query'].value.decode('utf-8')
            xl = xltrtr.transliterate(query)
            result = {'input': query, 'output': xl}
            print json.dumps(result)
        else:
            print 'Content-Type: text/html\n' # we'll be sending HTML instead

            f = open('web/frontend.html', 'r')
            html = f.read().decode('utf8')

            f = open('web/xltrtr.js', 'r')
            js = f.read()

            f = open('web/style.css', 'r')
            css = f.read()

            html = html.format(js = js, css = css)

            # if 'query' in args, compute transliteration and inject into
            # printed HTML, so it'll work on browsers with disabled js or xhr
            if 'query' in args:
                query = args['query'].value.decode('utf-8')
                xl = xltrtr.transliterate(query)

                template = find_template(html, 'translationtemplate')
                results = []

                top_score = xl[0]['score']
                for xl_result in xl:
                    if xl_result['score'] == top_score:
                        xl_result['iso'] = xl_result['iso639-1']
                        xl_result['result'] = xl_result['output']
                        results.append(template.format(**xl_result))

                def inject_after(text, to_inject, inject_after):
                    inject_loc = html.find(inject_after) + len(inject_after)
                    return text[:inject_loc] + to_inject + text[inject_loc:]

                results = ' or '.join(results)
                after = '<section id="translation">'
                html = inject_after(html, results, after)

                after = '<input type="text" name="query" id="query" value="'
                html = inject_after(html, query, after)

            print html.encode('utf8')

    # if we aren't CGI, assume command-line behaviour
    else:
        print 'please use xltrtr.py for command-line interface'
        print './xltrtr.py [string]'
        print '\ttransliterate string into best-guess of either Inuktitut or Russian'

