// Get references to elements
const addButton = document.getElementById('addButton');
const addButtons = document.querySelectorAll('.add-button');
const formOverlay = document.getElementById('formOverlay');
const closeFormButton = document.getElementById('closeForm');
const addPersonForm = document.getElementById('addPersonForm');
const personList = document.getElementById('personList');
const attendanceCreationForm = document.getElementById("attendance-creation");
attendanceOverlay = document.getElementById("formOverlay2");
const createNew = document.getElementById("createNew");
const closeForm2 = document.querySelector(".close-form");

const copyUrlBtn = document.querySelectorAll('button.copy').forEach(el=>{
  parent = el.parentElement;
  let url = el.getAttribute("data-url");
  el.addEventListener('click', function(ev){
    navigator.clipboard.writeText(location.origin + url + "/");
    ev.target.innerText = "Copied!";
    setTimeout(()=>ev.target.innerText = "Copy URL", 2000);
  })
})
createNew.addEventListener('click', function(e){
  attendanceOverlay.style.display = "flex";
})

closeForm2.addEventListener('click', function(e){
  e.preventDefault();
  attendanceOverlay.style.display = 'none';
})
// Event listener to open the form when "+" button is clicked
// addButton.addEventListener('click', () => {
//   formOverlay.style.display = 'flex';
// });

addButtons.forEach(elem=>elem.addEventListener('click', () => {
    formOverlay.style.display = 'flex';
  }));

// Event listener to close the form when "Close" button is clicked
closeFormButton.addEventListener('click', () => {
  formOverlay.style.display = 'none';
});

