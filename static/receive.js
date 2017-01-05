$( document ).ready(function() {

    var success = $('#successNotify').text();
    if(success.includes("presentation"))
    {

        $.notify({
            // options
            message: success
        },{
            // settings
            type: 'success',
            placement: {
                from: "top",
                align: "center"
            },
        });
    }
    if(success.includes("Try again"))
    {

        $.notify({
            // options
            message: success
        },{
            // settings
            type: 'danger',
            placement: {
                from: "top",
                align: "center"
            },
        });
    }

    
    //
    // Speech Recognition Methods
    //

    //
    // Check local storage for the correct UI output
    //

    window.onload = function() {
      if(sessionStorage.status == "ON")
    {
        $('#miced').removeClass("fa-microphone");
        $('#miced').addClass("fa-stop animated infinite pulse");
    }
    else if(sessionStorage.status == "OFF")
    {
        $('#miced').removeClass("fa-stop animated infinite pulse");
        $('#miced').addClass("fa-microphone");
    }
    else
    {
        $('#miced').removeClass("fa-stop animated infinite pulse");
        $('#miced').addClass("fa-microphone");
    }

};

if (!('webkitSpeechRecognition' in window)) {
            $('#mic').remove(); }
else
{
    var recognition = new webkitSpeechRecognition();
    var recognizing; //That is the object that will manage our whole recognition process. 
    recognition.continuous = true;   //Suitable for dictation. 
    recognition.interimResults = true;  //If we want to start receiving results even if they are not final.
    //Define some more additional parameters for the recognition:
    recognition.lang = "en-US"; 
    recognition.maxAlternatives = 1;    
    reset();

    $('#mic').click(function(){
		
		toggleStartStop();

        });

    //Stop function
}

    function reset() {
	recognizing = false;
	$('#miced').removeClass("fa-stop animated infinite pulse");
	$('#miced').addClass("fa-microphone");
	
}

function toggleStartStop()
{
	if(recognizing)
	{
		sessionStorage.status = "OFF";
		recognition.stop();
		$('#convo').val("");
		reset();
	}
	else
	{
		if (!('webkitSpeechRecognition' in window)) {
			alert("Speech recognition not available on this browser. Please choose another.")
    	//Speech API not supported here…
		} else { //Let’s do some cool stuff :)
		    //Since from our experience, the highest result is really the best...
		    recognition.start();
		    recognizing = true;
		    sessionStorage.status = "ON";
	        $('#miced').removeClass("fa-microphone");
			$('#miced').addClass("fa-stop animated infinite pulse");
		    recognition.onstart = function() {
		    //Listening (capturing voice from audio input) started.
		    //This is a good place to give the user visual feedback about that (i.e. flash a red light, etc.)

		 
		        
			};

		    recognition.onerror = function(event) {
		         recognition.start();
                recognizing = true;
                sessionStorage.status = "ON";
                $('#miced').removeClass("fa-microphone");
                $('#miced').addClass("fa-stop animated infinite pulse");
		    }

			recognition.onresult = function(event) { //the event holds the results
			//Yay – we have results! Let’s check if they are defined and if final or not:
		    if (typeof(event.results) === 'undefined') { //Something is wrong…
		        recognition.stop();
		        alert("This app has stopped listening.");
		        return;
		    }
		    var text = []
		    for (var i = event.resultIndex; i < event.results.length; ++i) {      
		        if (event.results[i].isFinal) { //Final results
		            console.log("final results: " + event.results[i][0].transcript);
		            	$('#convo').val(event.results[i][0].transcript);
		            	$("#find").trigger("click").delay(2000);

		        } else {   //i.e. interim...
		            console.log("interim results: " + event.results[i][0].transcript);
		            $('#convo').text(event.results[i][0].transcript);  //You can use these results to give the user near real time experience.
		        } 
		    } //end for loop


}; 


}
		
		
	}
}



});

