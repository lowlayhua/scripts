# index.php
```
<html>
<head><title>Welcome to my excellent blog</title></head>
<body>
<h1>Welcome to my excellent blog</h1>
<img src='https://storage.googleapis.com/qwiklabs-gcp-03-5b6877746ea8/my-excellent-blog.png'>
<?php
$dbserver = "35.202.248.xx";
$dbuser = "blogdbuser";
$dbpassword = "xxxxx";
// In a production blog, we would not store the MySQL
// password in the document root. Instead, we would store it in a
// configuration file elsewhere on the web server VM instance.
$conn = new mysqli($dbserver, $dbuser, $dbpassword);
if (mysqli_connect_error()) {
        echo ("Database connection failed: " . mysqli_connect_error());
} else {
        echo ("Database connection succeeded.");
}
?>
</body></html>
```
