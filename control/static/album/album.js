var albumApp = angular.module('albumApp', ['ngMaterial', 'akoenig.deckgrid', 'ngFileUpload']);

angular.module('albumApp').controller('AlbumController', AlbumController);

AlbumController.$inject = ['$scope', '$http', 'Upload', '$mdDialog'];

function AlbumController($scope, $http, Upload, $mdDialog) {
	$scope.albums = [];
	$scope.currentAlbum = {};
	$scope.images = [];

	$scope.upload = function (file) {
		Upload.upload({
			url: '/album/upload-image',
			data: {file: file, 'album': $scope.currentAlbum.path}
		}).then(
			function successCallback(response) {
				console.log(response);
				if (response.data == 'File uploaded') {
					console.log('Image successfully uploaded!');
					$scope.getImages($scope.currentAlbum);
				}
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.deleteImage = function (src) {
		$http.post('/album/delete-image', {image: src}).then(
			function successCallback(response) {
				console.log(response);
				if (response.data == 'File deleted') {
					console.log('Image successfully deleted');
					$scope.getImages($scope.currentAlbum);
				}
			},
			function errorCallback(response) {
				console.log('error!');
			});
	};

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
		if (album != $scope.currentAlbum) {
			$scope.currentAlbum = album;
			$scope.getImages($scope.currentAlbum);
		}
	};

	$scope.albumAddModal = function(ev) {
		var dialog = $mdDialog.prompt()
			.title('New Album')
			.placeholder('Album name')
			.ariaLabel('Album name')
			.targetEvent(ev)
			.ok('Okay')
			.cancel('Cancel');

		$mdDialog.show(dialog).then(function okCallback (albumName) {
			return $http.post('/album/new-album', {'albumName': albumName})
				.then(function successCallback(response) {
					console.log(response);
					if (response.data == 'Album created') {
						console.log('Album successfully created');
						$scope.getAlbums();
					}
				}, function errorCallback(response) {
					console.log('error!');
				});
		}, function cancelCallback () {
			console.log('Cancelled out');
		});
	};

	$scope.deleteAlbum = function (album) {
		return $http.post('/album/delete-album', {'path': album.path})
			.then(function successCallback(response) {
				console.log(response);
				if (response.data == 'Album deleted') {
					console.log('Album successfully deleted');
					$scope.getAlbums();
				}
			}, function errorCallback(response) {
				console.log('error!');
			});
	};

	$scope.getAlbums();
}