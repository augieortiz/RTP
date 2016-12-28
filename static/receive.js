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
                from: "bottom",
                align: "right"
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
                from: "bottom",
                align: "right"
            },
        });
    }

    

         
    if(localStorage.getItem("voice") == "on")
    {
        startSpeech();
    }


    $('#mic').click(function(){
        if (typeof(Storage) !== "undefined") {
        if(localStorage.getItem("voice") == "on")
        {
           localStorage.setItem("voice", "off");
            $('#mic').toggleClass("animated infinite pulse",function(){
               $(this).remove();
               });  
        }
        else
        {
        localStorage.setItem("voice", "on"); 
      	startSpeech();
      }
      }
        });       
});

function startSpeech (){
	if (!('webkitSpeechRecognition' in window)) {
		alert("Speech recognition not available on this browser. Please choose another.")
                 $('#mic').removeClass("animated infinite pulse");
    //Speech API not supported here…
} else { //Let’s do some cool stuff :)
    var recognition = new webkitSpeechRecognition(); //That is the object that will manage our whole recognition process. 
    recognition.continuous = true;   //Suitable for dictation. 
    recognition.interimResults = true;  //If we want to start receiving results even if they are not final.
    //Define some more additional parameters for the recognition:
    recognition.lang = "en-US"; 
    recognition.maxAlternatives = 1; //Since from our experience, the highest result is really the best...
    recognition.start();
    recognition.onstart = function() {
    //Listening (capturing voice from audio input) started.
    //This is a good place to give the user visual feedback about that (i.e. flash a red light, etc.)
          $("#mic").animate({color:'red'},1000);
         $('#mic').toggleClass("animated infinite pulse",function(){
               $(this).remove();
               if (typeof(Storage) !== "undefined") 
               {
                    localStorage.setItem("voice", "off");
                }
            });
	};

    recognition.onerror = function(event) {
         $("#mic").animate({color:'red'},1000);
         $('#mic').toggleClass("animated infinite pulse",function(){
               $(this).remove();
           });
         startSpeech();
    }

	recognition.onresult = function(event) { //the event holds the results
	//Yay – we have results! Let’s check if they are defined and if final or not:
    if (typeof(event.results) === 'undefined') { //Something is wrong…
        recognition.stop();
        alert("This app has stopped listening.");
        $('#mic').removeClass("animated infinite pulse");
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