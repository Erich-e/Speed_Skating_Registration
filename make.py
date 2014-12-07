import csv

out = open('ss.html', 'w')

f = csv.reader(open('ss.csv'))

out.write("<table style = 'width=100%>'")

for row in f:
	out.write('<tr>')
	for element in row:
		if len(element)!=0:
			if element[0] == '$':
				out.write("<td><input type='text' name='%s' style='display:table-cell; width:100%%'/></td>\n" %(element))
			elif element[0] == '[':
				choices = element[1:-1].split(',')
				out.write("<td><select name=%s>" %(choices[0]))
				for  i in range(1, len(choices)):
					out.write("<option value='%d'>%s</option>\n" %(i, choices[i]))
				out.write("</select></td>\n")
			elif element[0] == '!':
				out.write("<td><imput type = 'checkbox' name='%s' value='yes'/> %s <td>\n"%(element, element))
			elif len(element) != 0:
				out.write('<td> %s </td>\n' %(element))
	out.write('</tr>\n')

out.write("</table>")
