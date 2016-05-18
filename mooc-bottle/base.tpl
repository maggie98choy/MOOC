<html>
<title>List of courses</title>
<body>
<br/><br/>

<table border="1">
	<tr>
		<td>Category</td><td>Title</td><td>Section</td><td>Department</td><td>Term</td><td>Years</td><td>Instructor</td><td>Days</td><td>Hours</td><td>Description</td><td>Attachment</td><td>Version</td>
	</tr>


% for i in CourseList :
	<tr>
	<td>{{i['category']}}</td> <td>{{i['title']}}</td> <td>{{i['section']}}</td> <td>{{i['dept']}}</td><td>{{i['term']}}</td> <td><{{i["year"]}}</td> <td>{{i['instructor']}}</td> <td>{{i['days']}}</td> <td>{{i['hours']}}</td> <td>{{i['Description']}}</td> <td>{{i['attachment']}}</td> <td>{{i['version']}}</td>

	</tr>
        	
</table>
</body>
</html>
