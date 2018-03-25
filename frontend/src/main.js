import React from 'react';
import Home from './scenes/home/home';

class Main extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			imageURL: '',
		};

		this.handleUploadImage = this.handleUploadImage.bind(this);
	}

	handleUploadImage(ev) {
		ev.preventDefault();

		const data = new FormData();
		const filename = this.uploadInput.files[0].name;
		let extension = filename.split('.');
		extension = extension[extension.length - 1];
		data.append('file', this.uploadInput.files[0]);
		console.log(this.uploadInput.files[0]);
		data.append('filename', this.fileName.value);
		data.append('extension', extension);

		fetch('http://localhost:8000/upload', {
			method: 'POST',
			body: data,
		}).then((response) => {
			response.json().then((body) => {
				console.log({data: body.data });
				let isHotdog;
				if (body.data.labels) {
					let labels = body.data.labels.Labels;
					
					isHotdog = this.isHotdog(labels);
				}
				this.setState({ 
					imageURL: `http://localhost:8000/${body.file}`,
					isHotdog: isHotdog,
				});
			});
		});
	}

	isHotdog(labels) {

		for (let key in labels) {
			let label = labels[key];
			if (label.Name == 'Hot Dog') {
				return true;
			}
		}
		return false;
	}

	render() {
		return (
			<Home></Home>
		);
	}
}

export default Main;