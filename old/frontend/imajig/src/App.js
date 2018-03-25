import React, { Component } from 'react';
import {
	BrowserRouter as Router,
	Route
 } from 'react-router-dom';

import Home from './scenes/home/home';

class App extends Component {
  render() {
    return (
      <Router>
			<div style={{"minHeight": "100vh"}}>
				<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossOrigin="anonymous"></link>
				<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />
				<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossOrigin="anonymous"></script>
				<Route exact path="/" component={Home} />
			</div>
		</Router>
    );
  }
}

export default App;
