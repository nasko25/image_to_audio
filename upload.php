<?php
	
	$image_file_type = strtolower(pathinfo(basename($_FILES["fileToUpload"]["name"]),PATHINFO_EXTENSION));
	$dir = "uploads/";
	$file_name = $dir . substr("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", mt_rand(0, 51), 1).substr(md5(time()), 1) . "." . $image_file_type;
	$uploadOk = 1;

	echo $_POST["from"];
	echo $_POST["to"];
	error_log($_POST["from"]);
    error_log($_POST["to"]);
	echo $image_file_type;
	error_log(".".$image_file_type);
	
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
		
	if(file_exists($file_name)) {
            echo "File already exists. Try again later.";
            $uploadOk = 0;
    }

    if ($_FILES["fileToUpload"]["size"] > 500000) {
            echo "File too large.";
            $uploadOk = 0;
    }
	
	if((".".$image_file_type) !== $_POST["from"]&&!($_POST["from"]===".jpg"&&$image_file_type==="jpeg")) {
            echo "\nWrong file format.";
            $uploadOk = 0;
    }
	
	if ($uploadOk === 0) {
		echo "File was not uploaded.";
	}
    else {
            if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $file_name)) {
                echo "File has been uploaded";
                error_log("File ". basename($_FILES["fileToUpload"]["name"]) . " has been uploaded as ". $file_name);
				
				echo shell_exec(escapeshellcmd("./image_to_text.py"));
            }
            else {
				echo "Error uploading the file";
            }
	}
?>