<?php

	$dir = "server/uploads/";
	$uploadOk = 1;
	// Count # of uploaded files in array
	$total = count($_FILES["fileToUpload"]["name"]);

	echo $_POST["from"];
	echo $_POST["to"];
	error_log($_POST["from"]);
  	error_log($_POST["to"]);
	// echo $image_file_type;
	// error_log(".".$image_file_type);

	// error_log(print_r($_POST, TRUE));

	$use_pd = FALSE;
	$text_to_convert = "";

	if (isset($_POST["checkbox"]) && $_POST["checkbox"] === "on") {
		error_log("pd must be on");
		$use_pd = TRUE;
		error_log($use_pd);
	}

	for( $i=0 ; $i < $total ; $i++ ) {
		$image_file_type = strtolower(pathinfo(basename($_FILES["fileToUpload"]["name"][$i]),PATHINFO_EXTENSION));
		$file_name = $dir . substr("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", mt_rand(0, 51), 1).substr(md5(time()), 1) . "." . $image_file_type;

		 if(isset($_POST["submit"])||(isset($_FILES["fileToUpload"]))) {
		    // check if an image
		    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"][$i]);
				echo " " . $_FILES["fileToUpload"]["tmp_name"][$i];
		    $finfo = finfo_open(FILEINFO_MIME_TYPE); // return mime type ala mimetype extension
		    if($check !== false || finfo_file($finfo, $_FILES["fileToUpload"]["tmp_name"][$i]) === "application/pdf") {
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

	  if ($_FILES["fileToUpload"]["size"][$i] > 5000000) {
		  echo "File too large.";
		  $uploadOk = 0;
	  }

		// if((".".$image_file_type) !== $_POST["from"]&&!($_POST["from"]===".jpeg"&&$image_file_type==="jpg")) {
		//   echo "\nWrong file format.";
		//   $uploadOk = 0;
	  // }

		if ($uploadOk === 0) {
			echo "File was not uploaded.";
		}
	  else {
	    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"][$i], $file_name)) {
	        echo "File has been uploaded";
	        error_log("File ". basename($_FILES["fileToUpload"]["name"][$i]) . " has been uploaded as ". $file_name);
					// combine all the text from all photos
					if (!$use_pd)
						$text_to_convert .= shell_exec(escapeshellcmd("server/image_to_text.py " . $file_name));
					else
						$text_to_convert .= shell_exec(escapeshellcmd("server/image_to_text.py " . $file_name . " pd"));
	    }
	    else {
					echo "Error uploading the file";
	    }
		}
}

		$text_to_convert = $_POST["to"] . " " . $file_name . "\n\n" . $text_to_convert;
		file_put_contents($file_name . ".txt", $text_to_convert);
		echo "<br><br>" . $text_to_convert;
?>
