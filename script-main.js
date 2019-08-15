
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