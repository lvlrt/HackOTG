var system = require('system');
var fs = require('fs');
var args = system.args;
var page;

if (args.length === 1) {
	  console.log('Try to pass some arguments when invoking this script!');
} else {
var myurl=args[1]; 

var dump=args[2]; 
var dump_content;

var renderPage = function (url) {
	    page = require('webpage').create();
	    page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36';

	    page.onNavigationRequested = function(url, type, willNavigate, main) {
		            if (main && url!=myurl) {
				    		console.log("URL: "+url);
				    	if (url == "about:blank") {
						if (dump != "dump") {
				    		console.log(myurl);
						}
				    		}
				                myurl = url;
				    		
				                page.close()
				                setTimeout('renderPage(myurl)',1); //Note the setTimeout here
				            }
		        };

	    page.open(url, function(status) {
		    page.evaluate(function() {
			          });
		    	if (dump =="dump") {
				console.log(page.content);
			}
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
