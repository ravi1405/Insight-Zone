// Tabs
const loginTab = document.getElementById("login-tab");
const signupTab = document.getElementById("signup-tab");
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");

function confirmDelete(form_id){
  val = confirm("Do you really want to delete note?");
  var f = document.getElementById("delete-form-"+ form_id);
  console.log(val)
  if (val == false){
    f.setAttribute("action", "");
  } else {
    f.setAttribute("action", "/delete-note");
    f.submit();
  }

}
  function errorMessage(){
    var f = document.getElementById("save-form");
    console.log(f)
    title = document.getElementById("title").value;
    desc = document.getElementById("desc").value;
    pdf = document.getElementById("savenote").value;
    console.log(title, desc);
    c_path = window.location.href;
    console.log(c_path);
    if (title == "" || desc == "" || pdf == ""){
      alert("Not valid data");
      f.setAttribute("action", window.location.href);
    }
  }

function changeTab(tab) {
  debugger
  if (tab === "login") {
    if (window.location.href.indexOf("login") == -1){
        window.location.href = '/login/';
    }
    // loginTab.classList.add("active");
    // signupTab.classList.remove("active");
    // signupTab.classList.add("d-none");
    // loginForm.classList.remove("remove");
  } else {
    if (window.location.href.indexOf("register") == -1){
      window.location.href = '/register/';
    }
    // loginTab.classList.remove("active");
    // signupTab.classList.add("active");
    // signupForm.classList.remove("d-none");
    // signupTab.classList.add("d-none");
  }
}



