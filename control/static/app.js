var app = angular.module('app', ['ngMaterial']);

angular.module('app').controller('AppController', AppController);

AppController.$inject = ['$scope', '$http'];

function AppController($scope, $http) {
	$scope.imageEditShow = false;
	$scope.conf = {};
	$scope.albums = [];
	$scope.defaultAlbum = "";
	$scope.selectedAlbum = "";
	$scope.imgShuffleMins = 0;

	$scope.status = function () {
		return $http.post('/status').then(
			function successCallback(response) {
				console.log(response.data);	
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.reboot = function () {
		return $http.post('/reboot').then(
			function successCallback(response) {
				console.log(response.data);	
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.imageEdit = function () {
		if ($scope.imageEditShow) { $scope.imageEditShow = false; } else { 
			$scope.imageEditShow = true; }
	};

	$scope.getAlbums = function () {
		// Get list of albums via python, display them, set currentAlbum, call getImages
		return $http.get('/album/get-albums').then(
			function successCallback(response) {
				$scope.albums = response.data.albums;
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.imageShuffle = function () {
		if ($scope.selectedAlbum != '' && $scope.imgShuffleMins != 0) {
			$scope.conf.album = {name: $scope.selectedAlbum.name, path: $scope.selectedAlbum.path};
			$scope.conf.minBtwnShuffle = $scope.imgShuffleMins;
			return $http.post('/image-shuffle', {conf: $scope.conf}).then(
				function successCallback(response) {
					console.log(response);
				}, function errorCallback(repsonse) {
					console.log('error!');
				});
		}
	};

	$scope.getControlConf = function () {
		return $http.get('/get-control-conf').then(
			function successCallback(response) {
				console.log(response);
				if (response.data == 'No conf file found') {
					$scope.conf = { album: { name: '', path: ''}, minBtwnShuffle: 15};
					$scope.imgShuffleMins = $scope.conf.minBtwnShuffle;
				} else if (typeof response.data.conf === 'object') {
					$scope.conf = response.data.conf;
					$scope.defaultAlbum = response.data.conf.album;
					$scope.imgShuffleMins = response.data.conf.minBtwnShuffle;
				}
				
			}, function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.getControlConf();
	$scope.getAlbums();
}


