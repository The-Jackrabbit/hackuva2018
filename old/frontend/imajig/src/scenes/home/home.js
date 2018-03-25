import React, { Component } from 'react';

import SplashScreen from './scenes/splash';
import LoadingScreen from './scenes/load';
import ResultScreen from './scenes/result';



class Home extends Component {
	render() {
		return (
			<div>
				<SplashScreen></SplashScreen>
				<LoadingScreen></LoadingScreen>
				<ResultScreen></ResultScreen>
			</div>
		);
	}
}

export default Home;
