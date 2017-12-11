// ARG1: serve dir, ARG2: injection file
// node serve_and_inject.js tmp/SERVE/ tmp/inject.html
const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');
const util = require('util');
var querystring = require('querystring');
const port = 9000;
var serve_dir=process.argv[2]+"/"
var inject_file=process.argv[3]
var inject_updated=0
var inject_data=""
fs.stat(inject_file, function(err, stats){
    if(err) {
	    console.log('error reading injection file');
	    return;
    } else {
	inject_updated = new Date(util.inspect(stats.mtime));
	//update the contents of the inject_string
	fs.readFile(inject_file, function(err, data){
	    if(err){
		console.log("Error getting the file: ");
	    } else {
		inject_data=data;
	    }
	});
    }
});

http.createServer(function (req, res) {
	  console.log(`${req.method} ${req.url}`);
	console.log(req.rawHeaders);
	var body=""
	    req.on('data', function (data) {
		            body += data;
		        });

	    req.on('end', function () {
		            var post = querystring.parse(body);
		            console.log(post);
		        });

	  // parse URL
	  const parsedUrl = url.parse(req.url);
	  // extract URL path
	  var pathname = `.${parsedUrl.pathname}`;
	  // based on the URL path, extract the file extention. e.g. .js, .doc, ...
	  var ext = path.parse(pathname).ext;
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

	  fs.exists(serve_dir+pathname, function (exist) {
	      if(!exist) {
	      	pathname= '/index.html';
	  	ext = path.parse(pathname).ext;
	      }

	      if (fs.statSync(serve_dir+pathname).isDirectory()) {
		        pathname+= '/index.html';
	  		ext = path.parse(pathname).ext;
			fs.exists(serve_dir+pathname, function (exist) {
			      if(!exist) {
				pathname= '/index.html';
	  			ext = path.parse(pathname).ext;
			      }
			});
	      }

	      // read file from file system
	      var data = fs.readFile(serve_dir+pathname, 'utf8',function(err,data){
			//inject the html file here
			fs.stat(inject_file, function(err, stats){
			    if(err) {
				    console.log('error reading injection file');
				    return;
			    } else {
				    var tmp_date = new Date(util.inspect(stats.mtime));
				    if(inject_updated<tmp_date.getTime()){
					inject_updated=tmp_date.getTime()
					console.log("injection file reloaded");
					//update the contents of the inject_string
					fs.readFile(inject_file, function(err, data){
					    if(err){
						console.log("Error getting the file: ");
					    } else {
						inject_data=data;
					    }
					});
				    }
		            }
			});
			//TODO if ext is html inject the code in the right place
			// if the file is found, set Content-type and send data
			var headers= {'Content-type': map[ext] || 'text/plain', "Access-Control-Allow-Origin": "*"}
			res.writeHead(200, headers);
			//var data_file=string(data.split("</body>"));
			//res.end(data_file[0]+"</body>"+data_file[1]);
			//res.end(data.replace("</body>",injection_data+"</body>"));
		      	var data_file=String(data).split("</body>");
			res.end(data_file[0]+inject_data+"</body>"+data_file[1]);
		     });
	    });
}).listen(parseInt(port));

console.log(`Server listening on port ${port}`);

