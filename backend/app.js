const fs = require('file-system');

const express = require('express');
const path = require('path');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');
const cors = require('cors');

const app = express();
var base64Img = require('base64-img');

const AWS = require('aws-sdk');
AWS.config.loadFromPath('./config.json');
var s3 = new AWS.S3();
var Upload = require('s3-uploader');
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(fileUpload());
app.use('/public', express.static(__dirname + '/public'));

var client = new Upload('codedgaze', {
	aws: {
	  path: 'images/',
	  region: 'us-east-1',
	  acl: 'public-read'
	},
  
	cleanup: {
	  versions: true,
	  original: false
	},
  
	original: {
	  awsImageAcl: 'private'
	},
  
});


app.post('/upload', (req, res, next) => {
	// console.log(req);
	console.log('hello from node!');
	/*const { spawn } = require('child_process');
	const pyProg = spawn('python',['./test.py']);
	
	pyProg.stdout.on('data', function(data) {

		console.log(data.toString());

	});*/

	let imageFile = req.files.file;
	console.log('imageFile');
	var params = {
		Bucket: 'codedgaze',
		Key: req.body.filename,
		Body: 'data',
		ACL:'public-read'
	};
	console.log('params');
	// var data = base64Img.base64Sync(`./public/${req.body.filename}.${req.body.extension}`);
	/*var s3 = new AWS.S3();
	
	s3.client.putObject(params, function(err, params){
		if (err) { 
			console.log('Error uploading data: ', err); 
		} else {
			//console.log('succesfully uploaded the image!');
		}
	});*/
	console.log('goodbye from node!');
	imageFile.mv(`${__dirname}/public/${req.body.filename}.${req.body.extension}`, function(err) {
		if (err) {
			// return JSON.stringify(res.status(500).send(err));
		}
		res.json({file: `public/${req.body.filename}.${req.body.extension}`});
	});
	/*
	client.upload(`./public/${req.body.filename}.${req.body.extension}`, {}, function(err, versions, meta) {
		if (err) { throw err; }
	  
		versions.forEach(function(image) {
		  console.log(image.width, image.height, image.url);
		  // 1024 760 https://my-bucket.s3.amazonaws.com/path/110ec58a-a0f2-4ac4-8393-c866d813b8d1.jpg 
		});
	});*/
	


});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
	const err = new Error('Not Found');
	err.status = 404;
	next(err);
});

// error handler
app.use(function(err, req, res, next) {
	// set locals, only providing error in development
	res.locals.message = err.message;
	res.locals.error = req.app.get('env') === 'development' ? err : {};

	// render the error page
	res.status(err.status || 500);
	res.render('error');
});

app.listen(8000, () => {
	console.log('8000');
});

module.exports = app;