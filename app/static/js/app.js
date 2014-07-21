'use strict';

angular.module('myApp', ['ngRoute', 'truncate', 'nvd3ChartDirectives'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider)
		{
		    $routeProvider
			    .when('/', {templateUrl: '/static/partials/home.html', controller: 'Home'})
			    .when('/servers', {templateUrl: '/static/partials/servers.html', controller: 'Servers'})
					.when('/jobs', {templateUrl: '/static/partials/jobs.html', controller: 'Jobs'})
          .when('/report', {templateUrl: '/static/partials/report.html', controller: 'Report'})
          .when('/resources/server/:server_id', {templateUrl: '/static/partials/resources_server.html', controller: 'ResourcesServer'})
			    .otherwise({redirectTo: '/'});

		    $locationProvider.html5Mode(true);
		}
	]
);
