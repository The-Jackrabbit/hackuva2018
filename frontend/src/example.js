import React, { Component } from 'react';
import './member.css'; 
import axios from "axios";
import CastList from "../../Components/Cast-List/castList";
import CreditCircle from "../../Components/Credit-Circle/creditCircle";
import NavDownArrow from "../../Components/NavDownArrow/navDownArrow";
import { PieChart, Pie, Tooltip, Cell, BarChart, XAxis, YAxis, CartesianGrid, Legend, Bar, ComposedChart, Line, Area } from 'recharts';

class Member extends Component {
	constructor() {
		super();
		
		this.state = {
			"person": "",
			"profilePicUrl": "",
			"castlist": "",
			"wordCount": "",
			"uniqueWordCount": "",
			"partData": {
				"barCategories": [],
				"data": [],
				"piePartData": [],
				"pieAlbumData": []
			},
			"partColors": ['#0A2463', '#2176FF', '#33A1FD', '#3E92CC', '#134074', '#011638', '#78C0E0'],
			"albumColors": ['#F9CB40', '#FFA737', '#FF6A00', '#FDCA40'],
			"fullHeight": "",
			"fullWidth": ""
		}
	}
	componentWillMount() {
		this.setState({
			"fullHeight": window.innerHeight,
			"fullWidth": window.innerWidth
		})
		var urlArgs;
		if (this.props.location === undefined) {
			urlArgs = ['member', 'Kevin+Abstract'];
		} else {
			urlArgs = this.props.location.pathname.split("/");
		}
		var personArg = urlArgs[urlArgs.length - 1];
		this.setState({
			"person": personArg,
			"castlist": <CastList activeLink={personArg}></CastList>
		});
		var _this = this;

		// GET PROFILE PIC
		axios.get(`http://localhost:8001/api/person/pics/?size=lg&name=${personArg}`)
		.then(function(res){
			_this.setState({
				"profilePicUrl": res.data.result.picUrl
			});
		});

		// GET WORD COUNTS AND STATS
		axios.get(`http://localhost:8001/api/person/words/?name=${personArg}&minLength=5&n=15`)
		.then(function(res){
			
			let wordBarCategories = [];
			let albumCats = res.data.result.albumCategories;
			for (let i = 1 ; i < albumCats.length ; i++) {
				wordBarCategories.push(<Bar dataKey={albumCats[i]} fill={_this.state.albumColors[i]} />);
			}
			_this.setState({
				"wordCount": res.data.result.wordCount,
				"uniqueWordCount": res.data.result.uniqueWordCount,
				"words": res.data.result.words,
				"wordBarCategories": wordBarCategories
			});
		});
		

		// GET SONG PART STATS
		axios.get(`http://localhost:8001/api/memberPage/?name=${personArg}`)
		.then(function(res){
			_this.setState({
				"partData": res.data.result.partData
			});
		})
	}

	render() {
		
		return (
			<div className="member-page">
				<div className="member grid-container" id="sections" style={{"width": this.state.fullWidth, "height": this.state.fullHeight}}>
					<div className="header">
						{this.state.castlist}
					</div>
					
					<div className="body">
						
					
						<div className="profile">
							<CreditCircle 
								size="lg"
								strokeColor="#D8D8D8" 
								pathBase="http://localhost:8001" 
								iconUrl={this.state.profilePicUrl}
								imageKey="hi"
								key="hi">
							</CreditCircle>

						</div>
						
						<div className="quick-stats">
							<div className="quick-words">
								<h2>words: <span className="count">{this.state.wordCount}</span></h2>
								<h5>(unique): <span className="unique-count">{this.state.uniqueWordCount}</span></h5>
							</div>
							<div className="quick-parts">
								<span className="parts-title quick-title">parts: </span>	
								<PieChart width={250} height={200}>
									<Pie data={this.state.partData.piePartData} dataKey="value" nameKey="name" 
										cx="50%" cy="50%" innerRadius={0} outerRadius={70} 
										fill="#82ca9d" label 
										isAnimationActive={true}>
										{
											this.state.partData.piePartData.map((entry, index) => <Cell fill={this.state.partColors[index % this.state.partColors.length]}/>)
										}
									</Pie>
									<Tooltip/>
								</PieChart>
								
							</div>
							<div className="quick-albums">
								<span className="parts-title quick-title">songs: </span>	
								<PieChart width={250} height={200}>
									<Pie data={this.state.partData.pieAlbumData} dataKey="value" nameKey="name" 
										cx="50%" cy="50%" innerRadius={0} outerRadius={70} 
										fill="#82ca9d" label 
										isAnimationActive={true}>
										{
											this.state.partData.pieAlbumData.map((entry, index) => <Cell fill={this.state.albumColors[index % this.state.albumColors.length]}/>)
										}
									</Pie>
									<Tooltip/>
								</PieChart>
							</div>
						</div>

						<div className="section-nav">
							<a href="#sections">sections</a>
							<a href="#words">words</a>
							<a href="#songs">songs</a>
						</div>

						<div className="section-stats">
						
							<BarChart width={900} height={350} data={this.state.partData.data}
									margin={{top: 5, right: 30, left: 20, bottom: 5}}>
								<XAxis dataKey="name"/>
								<YAxis/>
								<CartesianGrid strokeDasharray="3 3"/>
								<Tooltip/>
								<Legend />
								<Bar dataKey="Saturation I" fill='#F9CB40' />
								<Bar dataKey="Saturation II" fill='#FFA737' />
								<Bar dataKey="Saturation III" fill='#FF6A00' />
							</BarChart>
						</div>
							
						
					</div>
					<div className="footer">
						<NavDownArrow></NavDownArrow>
					</div>
					
						
					
				</div>	
				<div className="word-stats grid-container" id="words" style={{"width": this.state.fullWidth, "height": this.state.fullHeight}}>
					<BarChart width={this.state.fullWidth} height={this.state.fullHeight} data={this.state.words}
							margin={{top: 5, right: 30, left: 20, bottom: 5}}>
						<XAxis dataKey="name"/>
						<YAxis/>
						<CartesianGrid strokeDasharray="3 3"/>
						<Tooltip/>
						<Legend />
						{this.state.wordBarCategories}
					</BarChart>
				</div>
				<div className="song-stats grid-container" id="songs" style={{"width": this.state.fullWidth, "height": this.state.fullHeight}}>

				</div>
			</div>
				
		);
	}
}

export default Member;


