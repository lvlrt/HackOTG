var system = require('system');
var args = system.args;
var page;

if (args.length === 1) {
	  console.log('Try to pass some arguments when invoking this script!');
} else {
var myurl=args[1]; 

var renderPage = function (url) {
	    page = require('webpage').create();
	    page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36';

	    page.onNavigationRequested = function(url, type, willNavigate, main) {
		            if (main && url!=myurl) {
				    	if (url == "about:blank") {
				    		console.log(myurl)

        /*
        for filename in os.listdir(directory+"/"+url):
            with open(directory+"/"+url+"/"+filename) as f:
                for line in f.readlines():
                    if "<meta" in line and '"refresh"' in line:
                        redirect=True
                        line=line.rstrip()
                        index= line.find("URL=")
                        if index != -1:
                            line=line[index:] # strip all till URL=

                        index= line.find('"')
                        if index != -1:
                            line=line[:index] # strip all till quote

                        index= line.find("'")
                        if index != -1:
                            line=line[:index] # strip all till single quote

                        index= line.find(";")
                        if index != -1:
                            line=line[:index] # strip all till semi

                        index= line.find(" ")
                        if index != -1:
                            line=line[:index] # strip all till space
                        redirect_url=line
        if redirects:
            #if redirects are found
            #TODO remove old url
            #delete previous
            p = Popen("rm -Rf "+directory+"/"+url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            for line in p.stdout.read().splitlines():
                print(line.decode("utf-8"))
            p.communicate()

            url=redirect_url #change url to redirected url found
        else:
            print("OK and no further redirects");
            #TODO rename to savename
            p = Popen("rm -Rf "+directory+"/"+savename+" && mv "+directory+"/"+url+" "+directory+"/"+savename, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            for line in p.stdout.read().splitlines():
                print(line.decode("utf-8"))
            p.communicate()
            break
	*/




				    		}
				                myurl = url;
				                page.close()
				                setTimeout('renderPage(myurl)',1); //Note the setTimeout here
				            }
		        };

	    page.open(url, function(status) {
		    page.evaluate(function() {
			          });
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
