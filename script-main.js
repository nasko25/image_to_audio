
function changeValue(e, image_or_audio) {
	let old_text = e.textContent;
	let new_text = e.parentNode.parentNode.childNodes[1].textContent;
	new_text = new_text.replace(/\s/g, '');
	e.textContent = new_text;
	e.parentNode.parentNode.childNodes[1].textContent = old_text + " ";
	if (image_or_audio === "image")
		document.getElementById("from").value = old_text;
	else if (image_or_audio === "audio")
		document.getElementById("to").value = old_text;
	console.log(e.parent);
}

function screenSizeChange() {
	// set the dropdown attribute
	var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
	var height = (window.innerHeight > 0) ? window.innerHeight : screen.height;

	if (width < 979) {
		for (i = 0; i < document.getElementsByClassName("dropdown").length; i++) {
			document.getElementsByClassName("dropdown")[i].childNodes[1].setAttribute("data-toggle", "dropdown");
		}
		document.getElementsByClassName("checkbox_text_dm")[0].innerHTML = "";
	}
	if (width > 979) {
		for (i = 0; i < document.getElementsByClassName("dropdown").length; i++) {
			document.getElementsByClassName("dropdown")[i].childNodes[1].removeAttribute("data-toggle");
		}
		document.getElementsByClassName("checkbox_text_dm")[0].innerHTML = "dark mode";
	}

	// remove the "drag and drop" visuals
	if (width < 960 || height < 550) {
		var paragraphs = document.getElementsByClassName("small-print");
		for (i = 0; i < paragraphs.length; i++){
			paragraphs[i].innerHTML = "";
			paragraphs[i].remove();
		}
		document.getElementsByClassName("arrow")[0].remove();
		document.getElementsByClassName("dragndrop")[0].remove();
	}
}

screenSizeChange();
window.onresize = screenSizeChange;

function dropHandler(ev) {
  console.log('File(s) dropped');

  // start the loading animation
  load_anim();

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    // Use DataTransferItemList interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (ev.dataTransfer.items[i].kind === 'file') {
        var file = ev.dataTransfer.items[i].getAsFile();
        console.log('... file[' + i + '] - ' + file.name + ' uploaded.');

        formData.append("fileToUpload[]", file);
        formData.append("from", document.getElementById("from").value);
        formData.append("to", document.getElementById("to").value);
      }
    }

    var url= "upload.php";
    xhr.open('POST', url, true);

    // when the file is received callback
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {

        // to stop the animation
        document.cookie="loaded=true; SameSite=Lax";

        // get the filename of the received file
        var disposition = xhr.getResponseHeader('Content-Disposition');
        if (disposition && disposition.indexOf('attachment') !== -1) {
            var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            var matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) {
                var filename = matches[1].replace(/['"]/g, '');
            }
        } else {
            return;
        }

        // this allows me to ask the user if they want to download the audio file
        a = document.createElement('a');
        a.href = window.URL.createObjectURL(xhr.response);

        a.download = filename || "unsuccessful";
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
	    }
  	}
		xhr.responseType = 'blob';
		xhr.send(formData);
  }
	// TODO older browsers?
	// else {
  //   // Use DataTransfer interface to access the file(s)
  //   for (var i = 0; i < ev.dataTransfer.files.length; i++) {
  //     console.log('... file[' + i + '] - ' + ev.dataTransfer.files[i].name + ' uploaded.');
	//   	XMLHttpRequest.send(ev.dataTransfer.files[i]);
  //   }
  // }
}
// https://www.w3schools.com/php/php_file_upload.asp
function dragOverHandler(ev) {
  console.log('File(s) in drop zone');

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}

// loader animation
function load_anim() {
  document.getElementsByClassName("container")[0].style.display = "none";
  document.getElementById("loader_backgrd").style.display = "inline";

	document.cookie="loaded=false; max-age=1; SameSite=Lax";
	var interval = setInterval(()=>{
		if (getCookie("loaded")) {
			document.getElementById("loader_backgrd").style.display = "none";
			document.getElementsByClassName("container")[0].style.display = "inline";
			document.cookie="loaded=false; max-age=1; SameSite=Lax";
			clearInterval(interval);
		}
	}, 2000);
}


function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
