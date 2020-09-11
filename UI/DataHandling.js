$(document).ready(function(e)){
  e.preventDefault();
  $.ajax({
    type:"GET",
    url:"data.txt",
    dataType: "text",
    success: function(data){alert(data);}
  });
});

function getCellData(data){
  alert("yo!");
}
