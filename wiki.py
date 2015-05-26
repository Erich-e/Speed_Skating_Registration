#!/usr/bin/env python

import sys, os

def sanitize(text):
	text = text.replace('<b>', '[b]')
	text = text.replace('</b>', '[/b]')
	text = text.replace('&', '&amp;')
	text = text.replace('<', '&lt;')
	text = text.replace('>', '&gt;')
	text = text.replace('[b]', '<b>')
	text = text.replace('[/b]', '</b>')
	text = text.replace('[i]', '<i>')
	text = text.replace('[/i]', '</i>')
	text = text.replace("'", '&quot;')
	return text

def _int(x):
	try:
		return int(x)
	except:
		return 0

def _processTable(result, table, widths):
	style = 'style="border:1px solid black; border-collapse:collapse"'
	result.append('<div align="center">')
	result.append('<table width="80%%" %s>' % style);
	twidth = 0
	for i in range(len(widths)):
		widths[i] = _int(widths[i])
		twidth += widths[i]

	ntd = 0
	for row in table:
		ntd = max(ntd, len(row))
	w = (100-twidth)/ntd
	for i in range(ntd):
		if i >= len(widths):
			widths.append(w)
		elif widths[i] == 0:
			widths[i] = w
	for row in table:
		result.append('<tr%s>' % style)
		while len(row) < ntd:
			row.append('')
		for i in range(ntd):
			result.append('<td width="%d%%" %s>%s</td>' % (widths[i], style, row[i]))
		result.append('</tr>')
	result.append('</table></div>')

def _cleanLine(line):
	line = ''.join(i for i in line if ord(i) < 128)
	return line.strip()

def _titleLine(line):
	img0 = line.find('[img]')
	img1 = line.find('[/img]')
	img = ''
	if img0 >= 0 and img1 > img0:
		img = line[img0+5:img1]
		img = '<img src="%s"/>' % img
		l0 = line[0:img0].strip()
		l1 = line[img1+6:].strip()
		if l0 and l1:
			text = '<td><h2>%s</h2></td><td>%s</td><td><h2%s</h2></td>' % (l0, img, l1)
		elif l0:
			text = '<td><h2>%s</h2></td><td align="right">%s</td>' % (l0, img)
		else:
			text = '<td>%s</td><td><h2>%s</h2></td>' % (img, l1)
	else:
		text = '<td><h2>%s</h2></td>' % line
	return '<table width=100%%><tr>%s</tr><td></table>' % text

def process(file):
	text = open(file, 'r').read()
	text = sanitize(text)
	lines = text.splitlines()
	i = 0
	result = ['<!-- Automatically generated HTML from wiki format-->\n']
	while i < len(lines):
		lines[i] = _cleanLine(lines[i])
		if len(lines[i]) == 0:
			result.append('<br/>')
		elif lines[i] == '----':
			result.append('<hr/>')
		elif lines[i][0] == '=':
			result.append(_titleLine(lines[i][1:]))
		elif lines[i][0] == '-':
			s = i
			e = i+1
			while e < len(lines) and len(lines[e]) and lines[e][0] == '-':
				e += 1
			if e - s > 1:
				result.append('<ul>')
				for j in range(s, e):
					result.append('<li>%s</li>' % lines[j].replace('-',''))
				result.append('</ul>')
				i = e-1
		elif lines[i] == '{|':
			table = []
			row = []
			widths = []
			i += 1
			while i < len(lines):
				if lines[i].startswith('|%'):
					widths = lines[i].split()[1:]
				elif lines[i] == '|-':
					table.append(row)
					row = []
				elif lines[i] == '|}':
					if row:
						table.append(row)
					_processTable(result, table, widths)
					break
				else:
					row.append(lines[i])
				i += 1
		else:
			result.append(lines[i])
		i += 1
	text = ' '.join(result)
	return text.replace('\n', ' ')

def test():
	text = process('/tmp/print.txt')
	print text

if __name__ == '__main__':
	test()
