<!-- result template -->

<!DOCTYPE html>
<html>

<head>
</head>

<body>
	<h3><p>Host added.</p></h3>
	<h3><p> <input type="button" value="Back" onclick="history.back(-1)" /> </p></h3>
	<h2><p>Hosts:</p></h2>
	
	<p>
		%for item in returnhosts:
			<tr>
				<td> {{item}} </td>
			</tr>
	</p>


</body>

</html>
