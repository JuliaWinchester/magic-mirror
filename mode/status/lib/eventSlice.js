eventSlice = function (events) {
	var yearOptions = [['BC',500], [501, 1000], [1001, 1500], [1501, 1750], [1751, new Date().getFullYear()]];
	var years = yearOptions[Math.floor(Math.random()*5)];
	var shortList = [];

	if (years[0] == 'BC') {
		for (var i = 0; i < events.length; i++) {
			if (events[i].year.indexOf('BC') > -1) {
				shortList.push(events[i]);
			} else {
				if (events[i].year <= years[1]) {
					shortList.push(events[i]);
				}
			}
		}	
	} else {
		for (var i = 0; i < events.length; i++) {
			if (years[0] <= events[i].year && events[i].year <= years[1]) {
				shortList.push(events[i]);
			}
		}
	}
		
	console.log(years);
	console.log(shortList);

	if (shortList.length > 0) {
		return shortList;
	} else {
		console.log('No events found for year range, re-sorting for new year range');
		return $scope.event(events);
	}
};