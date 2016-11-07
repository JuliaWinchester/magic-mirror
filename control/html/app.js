var app = angular.module('app', ['ngMaterial']);

angular.module('app').controller('AppController', AppController);

AppController.$inject = ['$scope', '$http'];

function AppController($scope, $http) {
	$scope.wake = function () {
		return $http.post('/wake', {key: 1337}).then(
			function successCallback(response) {
				return;	
			},
			function errorCallback(response) {
				return;
			});
	};

	$scope.sleep = function () {
		return $http.post('/sleep', {key: 1337}).then(
			function successCallback(response) {
				return;	
			},
			function errorCallback(response) {
				return;
			});
	};

	$scope.reboot = function () {
		return $http.post('/reboot', {key: 1337}).then(
			function successCallback(response) {
				return;	
			},
			function errorCallback(response) {
				return;
			});
	};
}

