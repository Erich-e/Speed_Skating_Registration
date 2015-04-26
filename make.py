import csv, sys, wiki, time, os

def safeout(out, text):
	out.write(wiki.sanitize(text))

def makePHP(filename='ss.php', formfile = 'ss.csv', amountfile = 'ss-amounts.csv', printfile = 'print.txt'):
	out = open(filename, 'w')

	out.write(open('head.html').read())
	colspan = 1
	fp = csv.reader(open(amountfile))
	f = []
	for row in fp:
		f.append(row)

	out.write('''
	<?php
	$nights = array(0, 0, 0, 0);
	$discounts = array(0, 0, 0, 0, 0);
	$family = array(0, 0, 0, 0, 0);
	''')
	for day in f:
		if len(day) > 0 and len(day[0]) > 0	and day[0][0] == '!':
			safeout(out, "$%s = array(0,0,0,0,0);\n" % (day[0][2:]))
	out.write('''
	function subtotal ($skater)
	{
	global $nights, $discounts, $family;
	$nights[$skater-1] = 0;
	$group = getvar('$GROUP'.$skater);
	$total = 0;
	''')
	for day in f:
		if len(day) > 0 and len(day[0]) > 0	and day[0][0] == '!':
			safeout(out, "global $%s; \n " % (day[0][2:]))
	for day in f:
		if len(day) > 0 and len(day[0]) > 0 and day[0][0] == '!':
			if day[0][1] == '_':
				safeout(out, '''if($nights[$skater-1] != 0) { ''')
			else:
				safeout(out, '''if(getvar("%s".$skater) == "checked") { ''' %(day[0]))
			if day[0][1] == '!':
				safeout(out, "$nights[$skater-1] = $nights[$skater-1] + 1 ;\n") 	
			for i in range(1, len(day)):
				safeout(out, '''if($group-1 == %d){ $total += %s; $%s[$skater]= %s; }\n''' %(i, day[i], day[0][2:], day[i])) 
			safeout(out, '}\n')
		if len(day) > 0 and len(day[0]) > 0 and day[0][0:9] == "%DISCOUNT":
			safeout(out, " $discounts[%s] = %s ; " %(day[0][-1], day[1]))
		if len(day) > 0 and len(day[0]) > 0 and day[0][0:7] == "%FAMILY":
			safeout(out, "$family[%s] = %s ; " %(day[0][-1], day[1]))
	out.write('''
	$total = $total - $discounts[$nights[$skater - 1]] - family($skater);
	return $total;
	}

	function family($skater)
	{
	global $family, $nights;
	if($nights[$skater-1] != 0)
		return $family[$skater];
	return 0;
	}

	function computeTotal()
	{
	printf("%g", subtotal(1)+subtotal(2)+subtotal(3)+subtotal(4));
	}
	subtotal(1);subtotal(2);subtotal(3);subtotal(4);
	?>
	''')

	out.write("<form>")
	out.write("<table style = 'width=100%>'")


	f = csv.reader(open(formfile))

	for row in f:
		out.write('<tr>')
		for element in row:
			element = wiki.sanitize(element)
			if len(element)==0:
				element = ' '
			if element[0] == '$':
				if not row[2]:
					colspan = 4 
				else:
					colspan = 1
				out.write('''<td colspan = "%d"><input type='text' name='%s' value="<?php showvar('%s');?>" style="width:100%%" /></td>\n''' %(colspan, element, element))
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
				out.write("<td><input type = 'checkbox' name='%s' value='checked'" % (pname))
				if element[1] == '_':
					checked = "if($nights[%s-1] != 0) printf('checked');" % (pname[-1])
					out.write(" disabled <?php %s ?> />"%(checked))
				else:
					checked = "showvar('%s');" % (pname)
					out.write(" <?php %s ?> />" % (checked))
				out.write(" %s ($<?php printf($%s[%s]); ?>) </td>\n" % (name, pname[2:-1], pname[-1]))
			elif element[0] == '%':
				skater = element[-1]
				if element[0:6] == '%TOTAL':
					out.write("<td> <?php computeTotal(); ?> </td>\n")
				elif element [0:7] == '%STOTAL':
					out.write("<td> <?php printf('%%g', subtotal(%s)); ?> </td>\n" % (element[-1]))
				elif element [0:9] == '%DISCOUNT':
					out.write("<td> -<?php printf('%%d', $discounts[$nights[%s-1]]); ?>  </td>\n" % (element[-1])) 
				elif element [0:7] == '%FAMILY':
					out.write("<td> -<?php printf('%%d', family(%s)); ?>  </td>\n" % element[-1]) 
				else:
					out.write('<td>ERROR - Unknown variable %s</td>' % element)
			else:
				out.write('<td> %s </td>\n' %(element))
				
		out.write('</tr>\n')

	out.write("</table>")
	out.write("<input type=submit value='recalculate'>")
	out.write("<input type=submit name='?Print' value = 'print'>")
	out.write('</form>')
	print_text = wiki.process(printfile)
	out.write("<?php if(getvar('?Print')=='print') printf('%%s', '%s')?>" % print_text)
	out.write(open('tail.html').read())
	out.write("</body></html>")

def confirmed(src, dest):
	if os.path.exists(src):
		bkp = dest + time.strftime('%Y%m%d-%H%M')
		if os.path.exists(dest):
			os.rename(dest, bkp)
		os.rename(src, dest)

def usage():
	print 'Invalid usage'
	sys.exit(1)

def main():
	if len(sys.argv) < 2:
		# usage()
		makePHP('ss.php', 'ss.csv', 'ss-amounts.csv', 'print.txt')
	elif sys.argv[1] == 'test' and len(sys.argv) == 5:
		#''' make.py test form.csv amount.csv print.txt '''
		makePHP('test.php', sys.argv[2], sys.argv[3], sys.argv[4])
	elif sys.argv[1] == 'confirm':
		confirmed('test.php', 'index.php')

main()
