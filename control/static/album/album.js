var albumApp = angular.module('albumApp', ['ngMaterial', 'akoenig.deckgrid']);

angular.module('albumApp').controller('AlbumController', AlbumController);

AlbumController.$inject = ['$scope', '$http'];

function AlbumController($scope, $http) {
	$scope.albums = [{name: 'name', path: 'album/'}, {name: 'name2', path: 'album2/'}];
	$scope.currentAlbum = {name: 'name', path: 'album/'};
	$scope.images = [];

	$scope.getAlbums = function () {
		// Get list of albums via python, display them, set currentAlbum, call getImages
		return $http.get('/album/get-albums').then(
			function successCallback(response) {
				$scope.albums = response.data.albums;
				$scope.setCurrentAlbum($scope.albums[0]);
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.getImages = function (album) {
		// For a given album object, get and display images via python
		config = {params: {path: $scope.currentAlbum.path}};
		return $http.get('/album/get-images', config).then(
			function successCallback(response) {
				console.log(response.data);
				$scope.images = response.data.images;
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.setCurrentAlbum = function (album) {
		$scope.currentAlbum = album;
		$scope.getImages($scope.currentAlbum);
	};

	$scope.getAlbums();
}