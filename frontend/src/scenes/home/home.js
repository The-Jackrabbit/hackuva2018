import React, { Component } from 'react';

import SplashScreen from './scenes/splash';
import LoadingScreen from './scenes/load';
import ResultScreen from './scenes/result';



class Home extends Component {
	render() {
		return (
			<div>
				<SplashScreen></SplashScreen>
			</div>
		);
	}
}

export default Home;
