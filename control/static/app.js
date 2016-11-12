var app = angular.module('app', ['ngMaterial']);

angular.module('app').controller('AppController', AppController);

AppController.$inject = ['$scope', '$http'];

function AppController($scope, $http) {
	$scope.status = function () {
		return $http.post('/status').then(
			function successCallback(response) {
				console.log(response);	
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.reboot = function () {
		return $http.post('/reboot').then(
			function successCallback(response) {
				console.log(response);	
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};
}

