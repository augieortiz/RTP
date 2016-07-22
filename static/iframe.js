$( document ).ready(function() {
  // Handler for .ready() called.
$("#frameDemo").load(function(){
  		$( "#frameDemo" ).contents().find( "a" ).css( "background-color", "#BADA55" );
	});
});