//TODO header CORS (see above
const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');
const port = process.argv[2] || 9000;

http.createServer(function (req, res) {
	  console.log(`${req.method} ${req.url}`);

	  // parse URL
	  const parsedUrl = url.parse(req.url);
	  // extract URL path
	  var pathname = `.${parsedUrl.pathname}`;
	  // based on the URL path, extract the file extention. e.g. .js, .doc, ...
	  const ext = path.parse(pathname).ext;
	  // maps file extention to MIME typere
	  const map = {
		      '.ico': 'image/x-icon',
		      '.html': 'text/html',
		      '.js': 'text/javascript',
		      '.json': 'application/json',
		      '.css': 'text/css',
		      '.png': 'image/png',
		      '.jpg': 'image/jpeg',
		      '.wav': 'audio/wav',
		      '.mp3': 'audio/mpeg',
		      '.svg': 'image/svg+xml',
		      '.pdf': 'application/pdf',
		      '.doc': 'application/msword'
		    };

	  fs.exists(pathname, function (exist) {
		      if(!exist) {
			      //TODO redirect to index?  
			            // if the file is not found, return 404
			            res.statusCode = 404;
			            res.end(`File ${pathname} not found!`);
			            return;
			          }

		      // if is a directory search for index file matching the extention
		  // TODO find a way to always serve the index file -> htm -> html -> php
		      if (fs.statSync(pathname).isDirectory()) pathname += '/index' + ext;

		      // read file from file system
		      fs.readFile(pathname, function(err, data){
			            if(err){
					            res.statusCode = 500;
					            res.end(`Error getting the file: ${err}.`);
				    } else {
						  // if the file is found, set Content-type and send data
						  //res.setHeader('Content-type', map[ext] || 'text/plain' );
					    	var headers= {'Content-type': map[ext] || 'text/plain', "Access-Control-Allow-Origin": "*"}
					    	res.writeHead(200, headers);
					    	//TODO inject the html file here (its a temporary one)
					    //TODO check if dnsspoof to this will catch all
						//TODO SNIPPET var xhtml = fs.readFileSync(__dirname + '/target_injected_xhtmljs_simple.html');
						  res.end(data);
						}
			          });
		    });
}).listen(parseInt(port));

console.log(`Server listening on port ${port}`);

