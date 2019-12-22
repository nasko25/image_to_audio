function on_dark_mode() {
  dark_mode_toogle = document.getElementById("dark_mode");
  // get <link rel="stylesheet" href="main.css">
  // maincss = document.getElementById("main_css");

  /* if (darkmode.checked == true){
    // change to dark_mode.css
    $('link[href="main.css"]').attr('href','dark_mode.css');
  } else {
    // change to main.css
    $('link[href="dark_mode.css"]').attr('href','main.css');
  } */

  if(dark_mode_toogle.checked == true && !document.getElementById('dark_mode_link')) {
    var dark_mode_link = document.createElement('link');
    dark_mode_link.rel = 'stylesheet';
    dark_mode_link.href = 'dark_mode.css';
    dark_mode_link.id = 'dark_mode_link';
    document.head.appendChild(dark_mode_link);
  }
  else {
    var dark_mode_id = document.getElementById("dark_mode_link");
    dark_mode_id.parentNode.removeChild(dark_mode_id);
  }
}
