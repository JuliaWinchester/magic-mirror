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

AppController.$inject = ['$scope', '$timeout', 'zipcode', '$http'];

function AppController($scope, $timeout, zipcode, $http) {
	$scope.tick = function () {
		$scope.date = new Date();
		$scope.dateplus = new Date($scope.date.getTime() + 86400000);
		$scope.dateplusplus = new Date ($scope.date.getTime() + 172800000);
		$timeout($scope.tick, 1000);
	};

	$scope.getWeather = function () {
		$http.jsonp('http://api.wunderground.com/api/56d8f038f0e507c9/conditions/forecast/hourly/q/27707.json?callback=JSON_CALLBACK').then(
			function successCallback(response) {
				console.log(response);
				var data = response.data;
				// Current data
				$scope.city = data.current_observation.display_location.city;
				$scope.state = data.current_observation.display_location.state;
				$scope.currentTemp = data.current_observation.temp_c;
				$scope.currentWeather = data.current_observation.weather;
				$scope.currentWeatherIcon = "wi-wu-" + data.current_observation.icon;
				var fc = response.data.forecast.simpleforecast.forecastday;

				// Daily forecast data
				$scope.dayHi = fc[0].high.celsius;
				$scope.dayLo = fc[0].low.celsius;
				
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
			},
			function errorCallback(response) {
				console.log('error!');
				console.log(response);
		});
	};

	$scope.getHistory = function () {
		historyData.load(function (response) {
			var events = eventSlice(response.Events);
			$scope.eventData = events[Math.floor(Math.random()*events.length)]; 
		});		
	};

	$scope.loop = function () {
		$scope.getWeather();
		$scope.getHistory();
		$timeout($scope.loop, 900000);
	};

	$scope.date = new Date();
	$scope.dateplus = new Date($scope.date.getTime() + 86400000);
	$scope.dateplusplus = new Date ($scope.date.getTime() + 172800000);
	$scope.tick();
	$scope.loop();


}