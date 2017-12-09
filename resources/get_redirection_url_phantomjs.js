var system = require('system');
var args = system.args;
var page;

if (args.length === 1) {
	  console.log('Try to pass some arguments when invoking this script!');
} else {
var myurl=args[1]; 

var renderPage = function (url) {
	    page = require('webpage').create();

	    page.onNavigationRequested = function(url, type, willNavigate, main) {
		            if (main && url!=myurl) {
				    		if (url == "about:blank") {
				    		console.log(myurl)
				    		}
				                myurl = url;
				                page.close()
				                setTimeout('renderPage(myurl)',1); //Note the setTimeout here
				            }
		        };

	    page.open(url, function(status) {
		            if (status==="success") {
				                    phantom.exit(0);
				            } else {
						                console.log("failed")
						                    phantom.exit(1);
						            }
		        });
} 

renderPage(myurl);
}
