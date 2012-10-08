#!/usr/bin/env python2.7
import sys
from pybtex.database.input import bibtex

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

ACCEPTED_TEMPLATE = '''                <tr>
                  <td>{0[number]}</td>
                  <td>
                    <p>{0[entry].fields[title]} <span class="label  label-important">{0[entry].fields[note]}</span><br/><strong><small>{0[authors]}</small></strong><br/><small>{0[entry].fields[booktitle]}, {0[entry].fields[month]} {0[entry].fields[year]}</small></p>
                  </td>
                </tr>'''
                
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
    
    parser = bibtex.Parser()
    bib_data = parser.parse_file(sys.argv[1])
    
    
    _keys = bib_data.entries.keys()
    _keys.reverse()
    _number = len(_keys)
    
    for _key in _keys:
        _entry = bib_data.entries[_key]
        _data = {'number': _number, 'entry': _entry}
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
            print reduce(lambda x, y: x.replace(y, TEX2TEXT[y]), TEX2TEXT, formatted)
        
        except KeyError, msg:
            print "Key error {0} for entry {1}".format(msg, _key)
        
#        print dir(bib_data.entries[_key]), _authors
#        print _data
        _number -= 1