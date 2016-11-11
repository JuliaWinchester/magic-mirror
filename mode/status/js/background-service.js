angular.module('app').service('BackgroundImg', BackgroundImg);

function BackgroundImg() {
	var service = {
		imgURL: '',
		imgDir: '../images/',
		imgFiles: {
			Clear: ['crystal_caves_day.gif','deep_forest_day.gif',
			'forest_edge_day.gif','jungle_waterfall_afternoon.gif',
			'jungle_waterfall_morning.gif','jungle_waterfall_night.gif',
			'magic_marsh_cave_night.gif','mirror_pond_afternoon.gif', 
			'mountain_fortress_dusk.gif','pond_ripples_day.gif',
			'seascape_day.gif','seascape_sunset.gif'],
			Cloudy: ['approaching_storm_day.gif','deep_swamp_day.gif',
			'harbor_town_night.gif','jungle_waterfall_afternoon.gif',
			'jungle_waterfall_night.gif','mountain_fortress_dusk.gif',
			'mountain_storm_day.gif','rough_seas_day.gif'],
			Rain: ['haunted_castle_ruins_rain.gif','highland_ruins_rain.gif',
			'jungle_waterfall_rain.gif','mirror_pond_rain.gif',
			'mountain_storm_day.gif'],
			Snow: ['mountain_stream_morning.gif','mountain_stream_night.gif',
			'winter_forest_snow.gif']
		},
		weatherCodes: {
			Clear: ['clear','partlysunny','sunny','mostlysunny','unknown'],
			Cloudy: ['cloudy','fog','hazy','mostlycloudy','partlycloudy'],
			Rain: ['chancerain','chancesleet','chancetstorms','sleet','rain','tstorms'],
			Snow: ['chanceflurries','chancesnow','flurries','snow']
		},
		setImg: function (weather) {
			console.log(weather);
			for (var key in service.weatherCodes) {
				if (service.weatherCodes.hasOwnProperty(key)) {
					if (service.weatherCodes[key].indexOf(weather) > -1) {
						var a = service.imgFiles[key];
						var f = a[Math.floor(Math.random()*a.length)];
						console.log(f);
						service.imgURL = service.imgDir + f;
						return service.imgURL;
					}
				}
			}
		}
	};
	return service;
}