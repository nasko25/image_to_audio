function on_dark_mode() {
  darkmode = document.getElementById("dark_mode");
  // get <link rel="stylesheet" href="main.css">
  maincss = document.getElementById("main_css");

  if (darkmode.checked == true){
    // change to dark_mode.css
    $('link[href="main.css"]').attr('href','dark_mode.css');
  } else {
    // change to main.css
    $('link[href="dark_mode.css"]').attr('href','main.css');
  }
}
