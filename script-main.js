
function changeValue(e) {
	let old_text = e.textContent;
	let new_text = e.parentNode.parentNode.childNodes[1].textContent;
	new_text = new_text.replace(/\s/g, '');
	e.textContent = new_text;
	e.parentNode.parentNode.childNodes[1].textContent = old_text + " ";
	console.log(e.parent);
}

function setDropdown() {
	var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
	if (width < 979) {
		for (i = 0; i < document.getElementsByClassName("dropdown").length; i++) {
			document.getElementsByClassName("dropdown")[i].childNodes[1].setAttribute("data-toggle", "dropdown");
		}
	} 
	if (width > 979) {
		for (i = 0; i < document.getElementsByClassName("dropdown").length; i++) {
			document.getElementsByClassName("dropdown")[i].childNodes[1].removeAttribute("data-toggle");
		}
	}
}

setDropdown();
window.onresize = setDropdown;

function dropHandler(ev) {
  console.log('File(s) dropped');

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (ev.dataTransfer.items[i].kind === 'file') {
        var file = ev.dataTransfer.items[i].getAsFile();
        console.log('... file[' + i + '] - ' + file.name + ' uploaded.');
		XMLHttpRequest.send(file); 
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.files.length; i++) {
      console.log('... file[' + i + '] - ' + ev.dataTransfer.files[i].name + ' uploaded.');
	  XMLHttpRequest.send(ev.dataTransfer.files[i]);
    }
  }
}
// https://www.w3schools.com/php/php_file_upload.asp
function dragOverHandler(ev) {
  console.log('File(s) in drop zone'); 

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}