<?php

	$dir = "server/uploads/";
	$uploadOk = 1;
	// Count # of uploaded files in array
	$total = count($_FILES["fileToUpload"]["name"]);

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
				error_log(" " . $_FILES["fileToUpload"]["tmp_name"][$i]);
		    $finfo = finfo_open(FILEINFO_MIME_TYPE); // return mime type ala mimetype extension
		    if($check !== false || finfo_file($finfo, $_FILES["fileToUpload"]["tmp_name"][$i]) === "application/pdf") {
		      error_log("File is an image or pdf- " . $check["mime"] . ".");
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
			exit();
		}
	  else {
	    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"][$i], $file_name)) {
	        error_log("File has been uploaded");
	        error_log("File ". basename($_FILES["fileToUpload"]["name"][$i]) . " has been uploaded as ". $file_name);
					// combine all the text from all photos
					if (!$use_pd)
						$text_to_convert .= shell_exec(escapeshellcmd("server/image_to_text.py " . $file_name));
					else {
						$text_to_convert .= shell_exec(escapeshellcmd("server/image_to_text.py " . $file_name . " pd"));
						unlink(explode(".", $file_name)[0] . "_thresh.png");
					}

					unlink($file_name);
	    }
	    else {
					error_log("Error uploading the file");
	    }
		}
}

		# $text_to_convert = $_POST["to"] . " " . $file_name . "\n\n" . $text_to_convert;
		// $text_to_convert = $text_to_convert;

		file_put_contents($file_name . ".txt", $text_to_convert);

		$uri = shell_exec(escapeshellcmd("server/text_to_audio.py " . $_POST["to"] . " " . $file_name . ".txt"));
		unlink($file_name . ".txt");

		$file_name = explode(".", $file_name)[0];
		$file_name = explode("/", $file_name)[2];
		header("Set-Cookie: loaded=true; Max-Age=15; SameSite=Lax");
		// TODO do the same about the other 3 possible audio formats
		if ($_POST["to"] === ".flac")
			header("Content-Type: audio/flac");
		else if ($_POST["to"] === ".wav")
			header("Content-Type: audio/wav");
		else if ($_POST["to"] === ".aiff")
			header("Content-Type: audio/aiff");
		else if ($_POST["to"] === ".m4a")
			header("Content-Type: audio/m4a");
		else
			header("Content-Type: audio/mpeg");
		header("Content-disposition: attachment;filename=" . $file_name . $_POST["to"]);
		error_log($uri);
		readfile($uri);
		// delete files
		unlink($uri);

		// header("Location: /" . $uri);
		exit();
?>
