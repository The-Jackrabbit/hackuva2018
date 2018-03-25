import React, { Component } from 'react';
import axios from 'axios';
import Logo from '../../../Assets/logo.svg';
import './splashscreen.css';
class SplashScreen extends Component {
	constructor(props) {
		super(props);

		this.state = {
			filePath: 'upload a zip ',
		};

		this.onChange = this.onChange.bind(this);
	}
	onChange(event) {
		console.log(event);
		console.log(event.target.value);
		this.setState({
			filePath: event.target.value,
		});
		this.handleUploadImage(event);
	}

	handleUploadImage(ev) {
		ev.preventDefault();

		const data = new FormData();
		data.append('datafile', this.uploadInput.files[0]);
		data.append('filename', ev.target.value);
		this.setState({
			data: data,
		});
		
		axios.post('http://localhost:8001/api/image/upload/', {
			datafile: this.uploadInput.files[0],
		})
			.then((response) => {
				response.json().then((body) => {
					this.setState({ imageURL: `http://localhost:8001/api/image/upload/${body.file}` });
				});
			})
			.catch(function (error) {
				console.log(error);
			});;
		
	}

	 
	render() {
		return (
			<div className="page-view grid splashscreen">
				<div className="logo">
					<img src={Logo} alt='imajig-logo'/>
				</div>
				<div className="links">
					<a href="#classify">Classify</a>
					<a href="#build">Build</a>
					<a href="#about">About</a>
				</div>
				<div className="form grid">
					<div className="search">
						<input type="text" className="search"/>
					</div>
					<div className="or">
						or...
					</div>
					<div className="upload">
						<span>{this.state.filePath}</span>
					</div>
					<div className="button">
						<label className="custom-file-upload">
							<input onChange={this.onChange} type="file" ref={(ref) => { this.uploadInput = ref; }} />
							file
						</label>
					</div>
				</div>
			</div>
		);
	}
}

export default SplashScreen;
