import csv

out = open('ss.html', 'w')

f = csv.reader(open('ss.csv'))

out.write(open('head.html').read())

out.write("<table style = 'width=100%>'")

for row in f:
	out.write('<tr>')
	for element in row:
		if len(element)==0:
			element = " "
		if element[0] == '$':
			out.write("<td><input type='text' name='%s' style='display:table-cell; width:100%%'/></td>\n" %(element))
		elif element[0] == '[':
			choices = element[1:-1].split(',')
			out.write("<td><select name=%s>" %(choices[0]))
			for  i in range(1, len(choices)):
				out.write("<option value='%d'>%s</option>\n" %(i, choices[i]))
			out.write("</select></td>\n")
		elif element[0] == '!':
			words = element.split()
			if(len(words)>1):
				name = ' '.join(words[1:])
			out.write("<td><input type = 'checkbox' name='%s' value='yes'/>%s</td>\n"%(element, name))
		else:
			out.write('<td> %s </td>\n' %(element))
			
	out.write('</tr>\n')

out.write("</table>")
out.write(open('tail.html').read())
