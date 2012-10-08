#!/usr/bin/env python2.7
"""
Project: https://github.com/cfedermann/research-page
 Author: Christian Federmann <cfedermann@dfki.de>
"""
import sys
from pybtex.database.input import bibtex

# BibTex-to-text mapping; non-exhaustive but complete wrt. bibliography.
TEX2TEXT = {
 '\\`{a}': '&agrave;',
 '\\"o': '&ouml;',
 '\\"a': '&auml;',
 '\\"u': '&uuml;',
 "\\'{c}": '&cacute;',
 "\\'{e}": '&eacute;',
 '{': '',
 '}': '',
}

# Template for accepted publications.
ACCEPTED_TEMPLATE = '''                <tr>
                  <td>{0[number]}</td>
                  <td>
                    <p>{0[entry].fields[title]} <span class="label  label-important">{0[entry].fields[note]}</span><br/><strong><small>{0[authors]}</small></strong><br/><small>{0[entry].fields[booktitle]}, {0[entry].fields[month]} {0[entry].fields[year]}</small></p>
                  </td>
                </tr>'''

# Template for published publications.                
PUBLISHED_TEMPLATE = '''                <tr>
                  <td>{0[number]}</td>
                  <td>
                    <p>{0[entry].fields[title]}<br/><strong><small>{0[authors]}</small></strong><br/><small>{0[entry].fields[booktitle]}, {0[entry].fields[address]}, {0[entry].fields[month]} {0[entry].fields[year]}</small><br/><span class="label">URL</span> <small><a href="{0[entry].fields[url]}">{0[entry].fields[url]}</a></small></p>
                  </td>
                </tr>'''

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print "\n\tusage: {0} <bib-file>\n".format(sys.argv[0])
        sys.exit(-1)
    
    PARSER = bibtex.Parser()
    BIB_DATA = PARSER.parse_file(sys.argv[1])
    
    
    KEYS = BIB_DATA.entries.keys()
    KEYS.reverse()
    NUMBER = len(KEYS)
    
    for _key in KEYS:
        _entry = BIB_DATA.entries[_key]
        _data = {'number': NUMBER, 'entry': _entry}
        _authors = []
        for person in _entry.persons['author']:
            _authors.append(u"{0} {1}".format(u" ".join(person.first()),
              u" ".join(person.last())))
              
        _data.update({'authors': u", ".join(_authors)})
        
        template = PUBLISHED_TEMPLATE 
        if _entry.fields.has_key('note'):
            template = ACCEPTED_TEMPLATE
        
        try:
            formatted = template.format(_data)
            print reduce(lambda x, y: x.replace(y, TEX2TEXT[y]), TEX2TEXT,
              formatted)
        
        except KeyError, msg:
            print "Key error {0} for entry {1}".format(msg, _key)
        
        NUMBER -= 1
