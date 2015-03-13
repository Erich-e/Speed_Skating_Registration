<html>
<head>
	<title> Registration Form Update</title>
</head>
<body>

<?php
$files = false;
function
getvar($name)
{
	return isset($_POST[$name])?$_POST[$name]:"";
}
function
getfile($name)
{
	return $_FILES[$name]["tmp_name"];
}
function
ftype($name)
{
	return pathinfo($_FILES[$name]["name"], PATHINFO_EXTENTION);
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
		if(/*ftype("Format") == ".csv" &&  ftype("Amounts") == ".csv" && ftype("Print") == ".txt"*/true)
		{
			$cmd = sprintf("python make.py test %s %s %s ", getfile("Format"), getfile("Amounts"), getfile("Print"));
			system($cmd);
			$files = true;
		}	
		else { ?>
			<script> alert("Wrong filetype \n Format - .csv \n Amounts - .csv \n Print - .txt"); </script>
		<?php } 
	}
	else{ ?>
		<script> alert("Incorrect Password");</script>
	<?php }
}
if(getvar("confirm") == "confirm")
{
	system("python make.py confirm");
}
?>

<div align="center">
	<h1>Toronto Speed Skating Club<h1>

	<table width="80%"><tr><td>
	This is the administration page for the Speed Skating Registration Form.
	Here, you can upload a new registration form template, new pricing
	information or a new text file for printing. <a href = 'help.html' terget = 'blank'>Help</a>
	</td></tr>
	<?php 
	if($files)
	{ ?>
		<tr><td> To verify your generated web page go to <a href = 'test.php' target = 'blank'>test site</a> Press confirm to save changes.</td></tr>
		<tr><td> <input type = "submit" value = "confirm" name = "confirm"> </td></tr>
	<?php }
	else
	{ ?>
	<tr><td>In order to upload these files, please enter the password you were given.</td></tr>
	</table> <table>
	<form action = "upload.php" method = "post" enctype = "multipart/form-data">
	<tr><td>Format: </td><td> <input type = "file" name = "Format"></td></tr>
	<tr><td>Amounts: </td><td> <input type = "file" name = "Amounts"></td></tr>
	<tr><td>Print: </td><td> <input type = "file" name = "Print"></td></tr>
	<tr><td>Password: </td><td> <input type = "password" name = "password"></td></tr>
	<tr><td> <input type = "submit" value =  "submit" name = "submit"></td></tr>
	<?php }
	?>
	<form>
	</td></tr></table>
</div>
</body>
</html>
