var app = angular.module('app', ['ngMaterial']);

angular.module('app').provider('zipcode', [function () {
	var zipcode = null;

	this.setZipcode = function (zip) {
		zipcode = zip;
	};

	this.$get = [function () {
		return zipcode;
	}];
}]);

angular.module('app').config(["zipcodeProvider", function (zipcodeProvider) {
	zipcodeProvider.setZipcode(27707);
	}]);

angular.module('app').controller('AppController', AppController);

AppController.$inject = ['$scope', '$timeout', 'zipcode', '$http', 'BackgroundImg', '$q'];

function AppController($scope, $timeout, zipcode, $http, BackgroundImg, $q) {
	$scope.tickLoop = function () {
		$scope.date = new Date();
		$scope.dateplus = new Date($scope.date.getTime() + 86400000);
		$scope.dateplusplus = new Date ($scope.date.getTime() + 172800000);
		$timeout($scope.tickLoop, 1000);
	};

	$scope.getWeather = function () {
		return $http.jsonp('http://api.wunderground.com/api/56d8f038f0e507c9/conditions/forecast/hourly/q/27707.json?callback=JSON_CALLBACK').then(
			function successCallback(response) {
				console.log(response);
				var data = response.data;
				if (data.response.hasOwnProperty('error')) {
					console.log('promise rejected');
					return $q.reject(data);
				} else {
					// Current data
					$scope.city = data.current_observation.display_location.city;
					$scope.state = data.current_observation.display_location.state;
					$scope.currentTemp = data.current_observation.temp_c;
					$scope.currentWeather = data.current_observation.weather;
					$scope.currentWeatherIcon = "wi-wu-" + data.current_observation.icon;
					
					// Daily forecast data
					var fc = response.data.forecast.simpleforecast.forecastday;
					$scope.dayWeatherIcon = fc[0].icon;
					$scope.dayHi = fc[0].high.celsius;
					$scope.dayLo = fc[0].low.celsius;
					
					// Hourly forecast data
					$scope.hourlyWeather = [];
					var hf = response.data.hourly_forecast;
					for (var i = 0; i < 8; i++) {
						$scope.hourlyWeather.push({
							time: new Date(hf[i].FCTTIME.epoch*1000),
							temp: hf[i].temp.metric,
							weather: hf[i].condition,
							weatherIcon: "wi-wu-" + hf[i].icon 
						});
					}
					console.log($scope.hourlyWeather);

					// Tomorrow forecast data
					$scope.tomorrowWeather = fc[1].conditions;
					$scope.tomorrowWeatherIcon = "wi-wu-" + fc[1].icon;
					$scope.tomorrowHi = fc[1].high.celsius;
					$scope.tomorrowLo = fc[1].low.celsius;

					// Day after tomorrow ("overmorrow") forecast data
					$scope.overmorrowWeather = fc[2].conditions;
					$scope.overmorrowWeatherIcon = "wi-wu-" + fc[2].icon;
					$scope.overmorrowHi = fc[2].high.celsius;
					$scope.overmorrowLo = fc[2].low.celsius;	
				}	
			},
			function errorCallback(response) {
				console.log('error!');
				console.log(response);
		});
	};

	$scope.initWeather = function () {
		$scope.getWeather().then(function successCallback() {
			$scope.backgroundLoop();
			console.log(BackgroundImg.imgURL);
		}, function errorCallback() {
			console.log('error!');
			$timeout($scope.initWeather, 10000);
		});
	};

	$scope.getHistory = function () {
		historyData.load(function (response) {
			var events = eventSlice(response.Events);
			$scope.eventData = events[Math.floor(Math.random()*events.length)]; 
		});		
	};

	$scope.dataLoop = function () {
		$scope.getWeather();
		$scope.getHistory();
		$timeout($scope.dataLoop, 900000);
	};

	$scope.backgroundLoop = function () {
		$scope.backgroundURL = BackgroundImg.setImg($scope.dayWeatherIcon);
		var msUntil5 = new Date($scope.date.getFullYear(), $scope.date.getMonth(), $scope.date.getDate(), 5, 0, 0, 0) - $scope.date;
		if (msUntil5 < 0) {
			msUntil5 += 86400000;
		}
		$timeout($scope.backgroundLoop, msUntil5);
	};

	$scope.date = new Date();
	$scope.dateplus = new Date($scope.date.getTime() + 86400000);
	$scope.dateplusplus = new Date ($scope.date.getTime() + 172800000);
	$scope.tickLoop();

	$scope.getHistory();
	$scope.initWeather();
	$timeout($scope.dataLoop, 900000);

}