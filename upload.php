<?php

	$dir = "uploads/";
	$file_name = $dir . substr("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", mt_rand(0, 51), 1).substr(md5(time()), 1);
	$uploadOk = 1;
	$image_file_type = strtolower(pathinfo(basename($_FILES["fileToUpload"]["name"]),PATHINFO_EXTENSION));

	echo $_POST["from"];
	echo $_POST["to"];
	echo $image_file_type;
	error_log($image_file_type);
	
	 if(isset($_POST["submit"])||(isset($_FILES["fileToUpload"]))) {
                // check if an image
                $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
                $finfo = finfo_open(FILEINFO_MIME_TYPE); // return mime type ala mimetype extension
                if($check !== false || finfo_file($finfo, $_FILES["fileToUpload"]["tmp_name"]) === "application/pdf") {
                        echo "File is an image or pdf- " . $check["mime"] . ".";
                        $uploadOk = 1;
                }
                else {
                        echo "File is not an image.";
                        $uploadOk = 0;
                }
        }
?>