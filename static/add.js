$( document ).ready(function() {

    $( "#deleteButton" ).click(function() {
     var sel = $("#instances option:selected").text();
     console.log(sel)
     $('#SI').text(sel);
     $("#inputSI").text(sel);
     $("#inputSI").val(sel);
  });
    $(function () {
  $('[data-toggle="tooltip"]').tooltip()
	});

	$("#addSpiderURL").submit(function() {
    $(this).submit(function() {
        return false;
    });
    return true;
});
});

function confirmDelete(documentID)
{
	
	$( "#cd" + documentID ).toggleClass( "hidden", 1000 , "easeOutSine" )
}

function validateForm()
{


  var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
  var regex = new RegExp(expression);
  var url = document.forms["addURL"]["url"].value;


    if (url.match(regex) )
   {
     return true;
   } 
   else {
     alert("This is not a valid URL");
     return false;
   }
 }

function validateSpiderForm()
{


  var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
  var regex = new RegExp(expression);
  var url = document.forms["addSpiderURL"]["url"].value;


    if (url.match(regex) )
   {
     $("#spinner").removeClass("hidden");
     $("#btnSpider").attr("disabled","disabled");
     return true;
   } 
   else {
     alert("This is not a valid URL");
     return false;
   }


 }