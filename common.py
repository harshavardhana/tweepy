# Tweepy
# Copyright 2010 Joshua Roesslein
# See LICENSE for details.

from datetime import datetime
import time
import htmlentitydefs
import re
import locale
from urllib import quote

try:
    from urllib.parse import parse_qs as compat_parse_qs
except ImportError: # Python 2
    # HACK: The following is the correct parse_qs implementation from cpython 3's stdlib.
    # Python 2's version is apparently totally broken
    def _unquote(string, encoding='utf-8', errors='replace'):
        if string == '':
            return string
        res = string.split('%')
        if len(res) == 1:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'replace'
        # pct_sequence: contiguous sequence of percent-encoded bytes, decoded
        pct_sequence = b''
        string = res[0]
        for item in res[1:]:
            try:
                if not item:
                    raise ValueError
                pct_sequence += item[:2].decode('hex')
                rest = item[2:]
                if not rest:
                    # This segment was just a single percent-encoded character.
                    # May be part of a sequence of code units, so delay decoding.
                    # (Stored in pct_sequence).
                    continue
            except ValueError:
                rest = '%' + item
            # Encountered non-percent-encoded characters. Flush the current
            # pct_sequence.
            string += pct_sequence.decode(encoding, errors) + rest
            pct_sequence = b''
        if pct_sequence:
            # Flush the final pct_sequence
            string += pct_sequence.decode(encoding, errors)
        return string

    def _parse_qsl(qs, keep_blank_values=False, strict_parsing=False,
                encoding='utf-8', errors='replace'):
        qs, _coerce_result = qs, unicode
        pairs = [s2 for s1 in qs.split('&') for s2 in s1.split(';')]
        r = []
        for name_value in pairs:
            if not name_value and not strict_parsing:
                continue
            nv = name_value.split('=', 1)
            if len(nv) != 2:
                if strict_parsing:
                    raise ValueError("bad query field: %r" % (name_value,))
                # Handle case of a control-name with no equal sign
                if keep_blank_values:
                    nv.append('')
                else:
                    continue
            if len(nv[1]) or keep_blank_values:
                name = nv[0].replace('+', ' ')
                name = _unquote(name, encoding=encoding, errors=errors)
                name = _coerce_result(name)
                value = nv[1].replace('+', ' ')
                value = _unquote(value, encoding=encoding, errors=errors)
                value = _coerce_result(value)
                r.append((name, value))
        return r

    def compat_parse_qs(qs, keep_blank_values=False, strict_parsing=False,
                encoding='utf-8', errors='replace'):
        parsed_result = {}
        pairs = _parse_qsl(qs, keep_blank_values, strict_parsing,
                        encoding=encoding, errors=errors)
        for name, value in pairs:
            if name in parsed_result:
                parsed_result[name].append(value)
            else:
                parsed_result[name] = [value]
        return parsed_result

def parse_datetime(string):
    # Set locale for date parsing
    previous_locale = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, 'C')

    # We must parse datetime this way to work in python 2.4
    date = datetime(*(time.strptime(string, '%a %b %d %H:%M:%S +0000 %Y')[0:6]))

    # Reset locale back to the default setting
    locale.setlocale(locale.LC_TIME, previous_locale)
    return date


def parse_html_value(html):

    return html[html.find('>')+1:html.rfind('<')]


def parse_a_href(atag):

    start = atag.find('"') + 1
    end = atag.find('"', start)
    return atag[start:end]


def parse_search_datetime(string):
    # Set locale for date parsing
    locale.setlocale(locale.LC_TIME, 'C')

    # We must parse datetime this way to work in python 2.4
    date = datetime(*(time.strptime(string, '%a, %d %b %Y %H:%M:%S +0000')[0:6]))

    # Reset locale back to the default setting
    locale.setlocale(locale.LC_TIME, '')
    return date


def unescape_html(text):
    """Created by Fredrik Lundh (http://effbot.org/zone/re-sub.htm#unescape-html)"""
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def convert_to_utf8_str(arg):
    # written by Michael Norton (http://docondev.blogspot.com/)
    if isinstance(arg, unicode):
        arg = arg.encode('utf-8')
    elif not isinstance(arg, str):
        arg = str(arg)
    return arg



def import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json  # Python 2.6+
        except ImportError:
            try:
                from django.utils import simplejson as json  # Google App Engine
            except ImportError:
                raise ImportError, "Can't load a json library"

    return json

def list_to_csv(item_list):
    if item_list:
        return ','.join([str(i) for i in item_list])

def urlencode_noplus(query):
    return '&'.join(['%s=%s' % (quote(str(k)), quote(str(v))) \
        for k, v in query.iteritems()])

