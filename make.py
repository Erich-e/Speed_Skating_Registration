import csv

out = open('ss.php', 'w')


out.write(open('head.html').read())

fp = csv.reader(open("ss-amounts.csv"))
f = []
for row in fp:
	f.append(row)


out.write('''
<?php
function subtotal ($skater)
{
$group = getvar('$GROUP'.$skater);
$total = 0;
''')
for day in f:
	if len(day) > 0 and len(day[0]) > 0 and day[0][0] == '!':
		out.write("if(getvar('%s'.$skater) == 'checked') { " %(day[0]))
		for i in range(1, len(day)):
			outswrite("if($group == %d) $total += %s;\n" %(i, day[i])) 
		out.write('}\n')

out.write('''
}
function computeTotal()
{
printf(subtotal(1)+subtotal(2)+subtotal(3));
}
?>
''')

out.write("<form>")
out.write("<table style = 'width=100%>'")


f = csv.reader(open('ss.csv'))

for row in f:
	out.write('<tr>')
	for element in row:
		if len(element)==0:
			element = " "
		if element[0] == '$':
			out.write("<td><input type='text' name='%s' value='<?php showvar('%s');?>' style='display:table-cell; width:100%%'/></td>\n" %(element, element))
		elif element[0] == '[':
			choices = element[1:-1].split(',')
			out.write("<td><select name=%s>" %(choices[0]))
			for  i in range(1, len(choices)):
				out.write("<option value='%d' <?php group('%s', %d);  ?> >%s</option>\n" %(i, choices[0], i, choices[i]))
			out.write("</select></td>\n")
		elif element[0] == '!':
			words = element.split()
			if(len(words)>1):
				name = ' '.join(words[1:])
			else:
				name = ''
			pname = words[0]
			out.write("<td><input type = 'checkbox' name='%s' value='checked' <?php showvar('%s');?> /> %s </td>\n"%(pname, pname, name))
		elif element[0] == '%':
			skater = element[-1]
			if element[0:6] == '%TOTAL':
				out.write("<td> <?php computeTotal(); ?> </td>\n")
			elif element [0:7] == '%STOTAL':
				out.write("<td> <?php subtotal(%s); ?> </td>\n" % element[-1])
			else:
				out.write('<td>ERROR - Unknown variable %s</td>' % element)
		else:
			out.write('<td> %s </td>\n' %(element))
			
	out.write('</tr>\n')

out.write("</table>")
out.write("<input type=submit value=submit>")
out.write('</form>')
out.write(open('tail.html').read())
