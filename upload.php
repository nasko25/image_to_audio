<?php

	$dir = "uploads/";
	$file_name = $dir . substr("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", mt_rand(0, 51), 1).substr(md5(time()), 1);
	$uploadOk = 1;
	$image_file_type = strtolower(pathinfo(basename($_FILES["fileToUpload"]["name"]),PATHINFO_EXTENSION));

	echo $_POST["from"];
	echo $_POST["to"];
	echo $image_file_type;
	error_log($image_file_type);
?>