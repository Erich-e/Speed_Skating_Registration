<html>
<head>
	<title> Registration Form Update</title>
</head>
<body>

<?php
function
getvar($name)
{
	return isset($_POST[$name])?$_POST[$name]:"";
}
function
getfile($name)
{
	return $_FILE[$name]["name"];
}
function
showvar($name)
{
	printf("%s", htmlspecialchars(getvar($name), ENT_QUOTES));
}
if(getvar("submit") == "submit")
{
	if(getvar("password") == "letmein")
	{
		
		

	}	
}
?>

<div align="center">
	<h1>Toronto Speed Skating Club<h1>

	<table width="80%"><tr><td>
	This is the administration page for the Speed Skating Registration Form.
	Here, you can upload a new registration form template, new pricing
	information or a new text file for printing.<p/>

	In order to upload these files, please enter the password you were given.</td></tr>
	</table> <table>
	<form action = "upload.php" method = "post">
	<tr><td>Format: </td><td> <input type = "file" name = "Format"></td></tr>
	<tr><td>Amounts: </td><td> <input type = "file" name = "Amounts"></td></tr>
	<tr><td>Print: </td><td> <input type = "file" name = "Print"></td></tr>
	<tr><td>Password: </td><td> <input type = "password" name = "password"></td></tr>
	<tr><td> <input type = "submit" value =  "submit" name = "submit"></td></tr>
	
	<form>
	</td></tr></table>
</div>
</body>
</html>
