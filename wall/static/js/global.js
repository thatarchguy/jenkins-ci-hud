$(document).ready(function() {

	$.getJSON("/api/v1/deploy", function(data) {
		$.each(data.deploys, function(i, item) {
			$('#deploys').append(
				'<div class="deploy" id="' + item.name + '">\
				 <h1>' + item.name +'</h1>\
				 <div id="' + item.name + '-date"></div>\
				 <div id="' + item.name + '-message"></div>');
		});
	});

	pollDeploy();
	pollBuild();
});


function pollDeploy(){
    $.get('/api/v1/deploy', function(data) {
    	$.each(data.deploys, function(i, item) {
    		if (item.phase == "STARTED"){
    			$('#'+item.name).css('background-color', '#311a88');
    			$('#'+item.name).pulseMe();
    			$('#'+item.name+'-date').html('<p>Started: ' + item.date_added + '</p>')
    		} else if (item.phase == "FINALIZED" || item.phase == "COMPLETED"){
    			if (item.status == "SUCCESS"){
    				$('#'+item.name).css('background-color', '#1A8831');
    				$('#'+item.name+'-date').html('<p>Last Deployed: ' + item.date_added + '</p>')
    			} else if (item.phase == "FAILURE"){
    				$('#'+item.name).css('background-color', '#CB2B2D');
    				$('#'+item.name+'-date').html('<p>Last Deployed: ' + item.date_added + '</p>')
    				$('#'+item.name+'-message').html('<p>Contact DEV NOW</p>')
    			}
    		}
    	});
	    setTimeout(pollDeploy,3000);
    });
}


$.fn.pulseMe = function() {
	this.delay(200).fadeTo('slow', .10).delay(50).fadeTo('slow', 1);
};


function pollBuild(){
	$.getJSON("/api/v1/ci", function(data) {
		$.each(data.builds, function(i, item) {
			if (findRow(item.number)) {
				row = findRow(item.number);
				/* touch each row first, so we know what to remove later */
				$(row).addClass("touched");
				if (item.status != $(row).find(".status").html()){
					if (item.status == "SUCCESS"){
	    				$(row).css('background', '#1A8831');
	    				$(row).find(".status").html("SUCCESS");
	    			} else if (item.status == "FAILURE"){
	    				$(row).css('background', '#CB2B2D');
	    				$(row).find(".status").html("FAILURE");
	    			}
				}
			} else{
				$('tbody').prepend('<tr class="touched" url="' + item.full_url + '">\
					<th scope="row" class="number">' + item.number + '</th>\
					<td>' + item.name + '</td>\
					<td>' + item.sourceBranch + '</td>\
	                <td>' + item.targetBranch + '</td>\
	                <td class="status">' + item.status + '</td>\
	                </tr>');
				if (item.phase == "STARTED"){
					row = findRow(item.number);
					$(row).css('background', '#311a88');
	    			$(row).pulseMe();
	    			$(row).click(function() {
 						window.location = $(this).attr("url")
 					});
	    		} else if (item.phase == "FINALIZED" || item.phase == "COMPLETED"){
	    			row = findRow(item.number);
	    			if (item.status == "SUCCESS"){
	    				$(row).css('background', '#1A8831');
	    			} else if (item.status == "FAILURE"){
	    				$(row).css('background', '#CB2B2D');
	    			}
	    		}
	    	}
		});
		/* remove the untouched! */
		$('tbody tr').each(function(){
			if (!$(this).hasClass("touched")) {
				$(this).fadeOut('slow', 
       				function(){ 
            			$(this).remove();                    
        			});
			}
			$(this).removeClass("touched");
		});
		setTimeout(pollBuild,3000);
	});
}


function findRow(text){
	$('tbody tr').each(function(){
        if($(this).find('.number').eq(0).text() == text){
        	row = this;
            return false;
        } else {
        	row = false;
        }
	 });
	return row;
}
