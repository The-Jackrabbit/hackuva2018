import React, { Component } from 'react';
import axios from 'axios';
import Logo from '../../../Assets/logo.svg';
import './splashscreen.css';
import { PieChart, Pie, Tooltip, Cell, BarChart, XAxis, YAxis, CartesianGrid, Legend, Bar, ComposedChart, Line, Area } from 'recharts';
import svgLogo  from './logo.svg';

import scrollToComponent from 'react-scroll-to-component';

class SplashScreen extends Component {

	constructor(props) {
		super(props);

		this.state = {
			filePath: 'upload an image',
			imageURL: '',
			file: null,
			wordBarCategories: null,
			loading: false,
			labelData: [],
			explicitLabelData: [],
			partColors: ['#FFEF7D', '#E53535', '#33A1FD', '#3E92CC', '#134074', '#011638', '#78C0E0'],
			albumColors: ['#FFEF7D', '#E53535', '#FF6A00', '#FDCA40'],
		};

		this.onChange = this.onChange.bind(this);
		this.handleUploadImage = this.handleUploadImage.bind(this);
		this.handleScrollToElement = this.handleScrollToElement.bind(this);
	}
	onChange(event) {
		this.setState({
			filePath: event.target.value,
			file: URL.createObjectURL(event.target.files[0]),
			touched: false,
			labelData: [],
			explicitLabelData: [],
			loading: false,

		});
	}

	handleUploadImage(ev) {
		ev.preventDefault();
		let randomFileName = () => {
			var text = '';
			var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
		 
			for (var i = 0; i < 10; i++)
			  text += possible.charAt(Math.floor(Math.random() * possible.length));
		 
			return text;
		};
		const data = new FormData();
		const filename = this.uploadInput.files[0].name;
		this.setState({
			loading: true,
		});
		let extension = filename.split('.');
		extension = extension[extension.length - 1];
		data.append('file', this.uploadInput.files[0]);
		console.log(this.uploadInput.files[0]);
		data.append('filename', randomFileName());
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
					let explicitLabels = body.data.explicitImageLabels.ModerationLabels;
					isHotdog = this.isHotdog(labels);
					let wordBarCategories = [];
					let data = [];
					let explicitLabelsData = [];
					let minConfidence = 100;
					for (let i = 0 ; i < labels.length ; i++) {
						let label = labels[i];
						label.value = label.Confidence;
						label.name = label.Name;
						if (label.value < minConfidence) {
							minConfidence = label.value;
						}
						data.push(label);
					}
					for (let i = 0 ; i < explicitLabels.length; i++) {
						let label = explicitLabels[i];
						label.value = label.Confidence;
						label.name = label.Name;
						if (label.value < minConfidence) {
							minConfidence = label.value;
						}
						explicitLabelsData.push(label);
					}
					console.log({
						wordBarCategories: wordBarCategories,
						data: data,
						isHotdog: isHotdog,
						labels: labels,
					});
					this.setState({
						labelData: data,
						explicitLabelData: explicitLabelsData,
						loading: false,
						minConfidence: Math.floor(minConfidence),
					});
				}
				
				this.setState({ 
					imageURL: `http://localhost:8000/${body.file}`,
					isHotdog: isHotdog,
					touched: true,
				});
				this.handleScrollToElement();
			});
		});
	}
 
	// without options
	
	 
	//with options

	isHotdog(labels) {

		for (let key in labels) {
			let label = labels[key];
			if (label.Name == 'Hot Dog' && label.Confidence > 40) {
				return true;
			}
		}
		return false;
	}

	handleScrollToElement(event) {
		scrollToComponent(this.isHotdogTitle, {align: 'top',});
	 }
	 
	render() {
		return (
			<div>
				<div className="page-view grid splashscreen">
					<div className="logo">
						<img src={Logo} alt='imajig-logo'/>
					</div>
					{/*<div className="links">
						<a href="#classify">Classify</a>
						<a href="#build">Build</a>
						<a href="#about">About</a>
					</div>*/}
					<div className="form grid">
						<form onSubmit={this.handleUploadImage}>
							<div className="file-submit-box grid" ref={(ref) => { this.fileSubmitBox = ref; }}>
								<div className="browse-box">
									<div className="file-select">
										<label className="custom-file-upload">
											file
											<input onChange={this.onChange} type="file" ref={(ref) => { this.uploadInput = ref; }} />
											
										</label>
									</div>
									<div className="file-path">
										<span>{this.state.filePath}</span>
									</div>
								</div>
								<div className="submit">
									<input type="submit" value="submit"/>
									
								</div>
							</div>
							<div className="results grid">
								<div className="source-image">
									{
										this.state.loading &&
										<div><img src={svgLogo} alt="loading-icon" className="loading-animation"/></div>
									}
									<img src={this.state.file} />
								</div>
								<div className="is-hotdog" ref={(ref) => { this.isHotdogTitle = ref; }} >

									{
										this.state.touched &&
										<h2>Hotdog?</h2>
									}
									{
										this.state.isHotdog && this.state.touched &&
											<p className="hotdog">Hotdog</p>
											
									}
									{
										(!this.state.isHotdog && this.state.touched &&
											<p className="not-hotdog">Not Hotdog</p>)
									}
									<div>
										{
											this.state.labelData.length > 0 &&
											<div>
												<h2>Label Data</h2>
												<BarChart data={this.state.labelData} height={500} width={500}
													margin={{top: 5, right: 30, left: 20, bottom: 5}}>
													<XAxis dataKey="name"/>
													<YAxis domain={[0, 100]}/>
													<CartesianGrid strokeDasharray="3 3"/>
													<Tooltip/>
													<Legend />
													<Bar  dataKey='value' fill={this.state.albumColors[0]} />
												</BarChart>
											</div>
											
										}
										{
											this.state.explicitLabelData.length > 0 &&
											<div>
												<h2>Adult Content</h2>
												<BarChart data={this.state.explicitLabelData} height={500} width={500}
													margin={{top: 5, right: 30, left: 20, bottom: 5}}>
													<XAxis dataKey="name"/>
													<YAxis domain={[0, 100]}/>
													<CartesianGrid strokeDasharray="3 3"/>
													<Tooltip/>
													<Legend />
													<Bar  dataKey='value' fill={this.state.albumColors[1]} />
												</BarChart>
											</div>
										}
										
									</div>
								</div>
								
								
							</div>
							
						</form>
					</div>
					
				</div>
			</div>
		);
	}
}

export default SplashScreen;
