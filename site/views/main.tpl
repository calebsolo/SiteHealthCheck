<!-- main template -->

<!DOCTYPE html>
<html>

<head>
</head>

<body>
	<h2><p>Submit New Host:</p></h2>
	<p>Please enter the full URL of the host to monitor:</p>
	
	<form action="/addhost" method="POST">   
		<input type="text" name="host" size=40 value=""><br><br>
			<input type="submit" value="Submit"><br>
	</form>


	<h2><p>Hosts:</p></h2>
	
	<p>
		%for item in returnhosts:
			<tr>
				<td> {{item}} </td>
			</tr>
	</p>
	
</body>

</html>
