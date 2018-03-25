const fs = require('file-system');

const express = require('express');
const path = require('path');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const {bucketName, region, accessKeyId, secretAccessKey } = require('./api_key.js');
const app = express();
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

/*
AKIAJHQVKO44SJVGALWQ
tbaVf9OnTLiISEzVFuGPTUBt5+NIGyvV/5vrG8Qp
*/

app.post('/upload', (req, res, next) => {
	// console.log(req);
	let jsondata = {};
	let imageFile = req.files.file;
	imageFile.mv(`${__dirname}/public/${req.body.filename}.${req.body.extension}`, function(err) {
		if (err) {
			// return JSON.stringify(res.status(500).send(err));
		}
	});

	console.log({
		'req.body.filename': req.body.filename,
		'req.body.extension': req.body.extension,
	});

	var AWS = require('aws-sdk');

	AWS.config.region = region;
	AWS.config.secretAccessKey = secretAccessKey;
	AWS.config.accessKeyId = accessKeyId;

	var uploadParams = {
		'Bucket': bucketName,
		'Key': `uploads/images/${req.body.filename}.${req.body.extension}`,
		'Body': req.files.file.data,
		'ContentEncoding': 'base64', 
		'Metadata': {
			'Content-Type': 'image/jpeg'
		}
	};
	var s3 = new AWS.S3();
	let imageLabels;
	let explicitImageLabels;

	let uploadPromise = function() {
		return new Promise(function(resolve, reject) {
			console.log('starting upload');
			let isResolved = false;
			let errorReport = {};
			var upload = s3.upload(uploadParams, function(err, data){
				if (err) reject(); // an error occurred
				else     isResolved=true;  
			});
			upload.on('httpUploadProgress', function (progress) {
				console.log(progress.loaded + ' of ' + progress.total + ' bytes');
				setTimeout(resolve(), 10000);
			});
			upload.send();
			 
		});
	};

	let listItemsPromise = function() {
		return new Promise(function(resolve, reject) {
			console.log('starting list items');
			s3.listObjects({
				'Bucket': bucketName,
			}, function(err, data){
				if (err) reject(); // an error occurred
				else     console.log({
					func: 'listObjects',
					data: data,
				});  
			});
			resolve();
			 
		});
	};

	let labelsPromise = function() {
		return new Promise(function(resolve, reject) {
			console.log('starting labels');
			var rekognition = new AWS.Rekognition();
			/* This operation detects labels in the supplied image */
			var labelParams = {
				Image: {
					S3Object: {
						'Bucket': bucketName, 
						'Name': `uploads/images/${req.body.filename}.${req.body.extension}`,
					}
				}, 
				MaxLabels: 123, 
				MinConfidence: 20
			};
			rekognition.detectLabels(labelParams, function(err, data) {
				if (err) {
					console.log({
						labelParams: JSON.stringify(labelParams),
						'req.body.filename': req.body.filename,
						'req.body.extension': req.body.extension,
						bucketName: bucketName,
						'uploads/images/${req.body.filename}.${req.body.extension}': `uploads/images/${req.body.filename}.${req.body.extension}`,
					});
					reject(err, err.stack); // an error occurred
				}
				else {
					imageLabels = data;
					resolve();
				}           // successful response
			});
		});
	};

	let explicitLabelsPromise = function() {
		return new Promise(function(resolve, reject) {
			
			console.log('starting explicitLabelsPromise');
			var rekognition = new AWS.Rekognition();
			var explicitLabelParams = {
				Image: {
					S3Object: {
						'Bucket': bucketName, 
						'Name': `uploads/images/${req.body.filename}.${req.body.extension}`,
					}
				}, 
			};
			rekognition.detectModerationLabels(explicitLabelParams, function(err, data) {
				if (err) reject(err, err.stack); // an error occurred
				else {
					explicitImageLabels = data;
					resolve();
				}
			});
		});
	};

	let renderPromise = function() {
		return new Promise(function(resolve, reject) {
			console.log('starting render');
			jsondata['labels'] = imageLabels;
			jsondata['explicitImageLabels'] = explicitImageLabels;
			res.json({file: `public/${req.body.filename}.${req.body.extension}`, data: jsondata});
			resolve();
		});
	};

	
	listItemsPromise().then(function(result) {
		return uploadPromise(result);
	}).then(function(result) {
		return listItemsPromise(result);
	}).then(function(result) {
		return labelsPromise(result);
		// return labelsPromise(result);
	}).then(function(result) {
		return explicitLabelsPromise(result);
	}).then(function(result) {
		return renderPromise(result);
	});


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

var server = app.listen(8000, () => {
	console.log('8000');
});
server.timeout = 10000;
module.exports = app;