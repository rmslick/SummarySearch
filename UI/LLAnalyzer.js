function GetProjDescription()
{
  var projectDescription = document.getElementById("projectDescription").value;
  var showText = document.getElementById("myTextArea");
  showText.value = projectDescription;
  document.getElementById("projectDescription").value = " ";
}

function GetFormInput()
{
  var title = document.getElementById("LessonTitle").value;
  var id    = document.getElementById("LessonId").value;

  var m11   = document.getElementById("mm1").value;
  var d1    = document.getElementById("dd1").value;
  var y1    = document.getElementById("yyyy1").value;

  var m2   = document.getElementById("mm2").value;
  var d2   = document.getElementById("dd2").value;
  var y2   = document.getElementById("yyyy2").value;

  var organization = document.getElementById("organization").value;

}
