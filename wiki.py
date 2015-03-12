#!/usr/bin/env python

import sys, os

_BIG = 9999

def sanitize(text):
	text = text.replace('<b>', '[b]', _BIG)
	text = text.replace('</b>', '[/b]', _BIG)
	text = text.replace('&', '&amp;', _BIG)
	text = text.replace('<', '&lt;', _BIG)
	text = text.replace('>', '&gt;', _BIG)
	text = text.replace('[b]', '<b>', _BIG)
	text = text.replace('[/b]', '</b>', _BIG)
	text = text.replace('[i]', '<i>', _BIG)
	text = text.replace('[/i]', '</i>', _BIG)
	text = text.replace("'", '&quot;', _BIG)
	return text

def process(file):
	text = open(file, 'r').read()
	text = sanitize(text)
	lines = text.splitlines()
	i = 0
	while i < len(lines):
		lines[i] = lines[i].strip()
		if len(lines[i]) == 0:
			lines[i] = '<p/><br/>'
		elif lines[i] == '----':
			lines[i] = '<hr/>'
		elif lines[i][0] == '=':
			lines[i] = '<h2>' + lines[i][1:] + '</h2>'
		elif lines[i][0] == '-':
			s = i
			e = i+1
			while e < len(lines) and lines[e][0] == '-':
				e += 1
			if e - s > 1:
				lines[s] = '<ul><li>%s</li>' % lines[s].replace('-', '')
				for j in range(s+1, e):
					lines[j] = '<li>%s</li>' % lines[j].replace('-','')
				lines[e-1] += '</ul>'
				i = e-1
		i += 1
	blurb = '<!-- Automatically generated HTML from wiki format-->\n'
	text = blurb + '\n'.join(lines)
	return text.replace('\n', ' ', _BIG)

def test():
	text = process('print.txt')
	print text

if __name__ == '__main__':
	test()
