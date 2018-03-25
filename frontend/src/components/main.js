import React from 'react';

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
				this.setState({ imageURL: `http://localhost:8000/${body.file}` });
			});
		});
	}

	render() {
		return (
			<form onSubmit={this.handleUploadImage}>
				<div>
					<input ref={(ref) => { this.uploadInput = ref; }} type="file" />
				</div>
				<div>
					<input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
				</div>
				<br />
				<div>
					<button>Upload</button>
				</div>
				<img src={this.state.imageURL} alt="img" />
			</form>
		);
	}
}

export default Main;