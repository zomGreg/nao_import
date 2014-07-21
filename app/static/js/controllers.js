'use strict';

/* Controllers */
angular.module('myApp')
	.controller('Home', ['$scope', '$http', '$filter', function($scope, $http, $q) {
		$scope.dt = new Date();

		$http({method: 'GET', url: '/api/servers?state=RUNNING'}).
			success(function(data, status, headers, config) {
				$scope.active_server_count = data.total_count;
			});

		$http({method: 'GET', url: '/api/cloud_accounts?activeOnly=true'}).
			success(function(data, status, headers, config) {
				$scope.cloud_account_count = data.total_count;
			});

		$http({method: 'GET', url: '/api/active_users_count'}).
			success(function(data, status, headers, config) {
				$scope.active_users_count = data.results[0].count;
			});

        $http({method: 'GET', url: '/api/budgets?activeOnly=true'}).
            success(function(data, status, headers, config) {
                $scope.active_budgets = data.total_count;
            });

		$http({method: 'GET', url: '/api/server_count_by_region'}).
            success(function(data, status, headers, config) {
                    $scope.regionData = data.results;
            });

		$http({method: 'GET', url: '/api/top_users_server_launch'}).
            success(function(data, status, headers, config) {
                    $scope.topUsers = data.results;
            });

		$http({method: 'GET', url: '/api/server_owned_count'}).
            success(function(data, status, headers, config) {
                    $scope.unique_server_owners = data.results[0].count;
            });

		$http({method: 'GET', url: '/api/server_event_location'}).
			success(function(data, status, headers, config) {
				if (data.results[0].location == 'internal') {
						$scope.internal_launches = data.results[0].count;
						$scope.external_launches = data.results[1].count;
				}
				else
				{
					$scope.internal_launches = data.results[1].count;
					$scope.external_launches = data.results[0].count;
				}
			});

		$http({method: 'GET', url: '/api/min_max_server_launch'}).
			success(function(data, status, headers, config) {
				$scope.last_launch = data.results[0].last_launch;
				$scope.first_launch = data.results[0].first_launch;
			});

        $scope.xAxisTickFormat = function(){
            return function(d){
                return d3.time.format('%Y-%m-%d')(new Date(d));
            }
        }

		$scope.yAxisTickFormat = function(){
            return function(d){
                return d3.format(',.2f');
            }
		}

		$scope.xFunction = function(){
            return function(d){
                return d.x;
            }
		}

		$scope.xFunctionPie = function(){
		    return function(d) {
		        return d.key+"         ";
		    };
		}

		$scope.yFunction = function(){
            return function(d){
                return d.y;
            }
		}

        $scope.$on('tooltipShow.directive', function(angularEvent, event){
            console.log('elementClick', arguments);
            angularEvent.targetScope.$parent.event = event;
            angularEvent.targetScope.$parent.$digest();
        });

        		$scope.$on('$viewContentLoaded', function ()
		{
			$scope.allTime();
		});

		$scope.allTime = function() {
			$('.loading').show();
			$('#morris-chart-area').empty();

			$http({method: 'GET', url: '/api/server_action_grouped'}).
				success(function(data, status, headers, config) {
					Morris.Area({
						element: 'morris-chart-area',
						data: data.results,
						lineColors: ['#EF1818','#0085C5'],
                        xLabels: "month",
						xkey: 'd',
						ykeys: ['terminations', 'launches'],
						labels: ['Terminations', 'Launches'],
						smooth: true
					});

					$('.loading').hide();
				});
		};

//		$scope.$on('$viewContentLoaded', function (){
//			$scope.serverAction(0);
//		});
//
//		$scope.serverAction = function(days) {
//			if (days > 0)
//			{
//				var url='/api/server_action?action=CREATE&days='+days
//			}
//			else
//			{
//				var url='/api/server_action?action=CREATE'
//			}
//
//			$http({method: 'GET', url: url}).
//				success(function(creates) {
//					$scope.serverCreates = {values: creates.results, key: 'Launch', color: '#1dff00', area: true}
//
//					if (days > 0)
//					{
//						var url='/api/server_action?action=DELETE&days='+days
//					}
//					else
//					{
//						var url='/api/server_action?action=DELETE'
//					}
//
//					$http({method: 'GET', url: url}).
//						success(function(deletes) {
//							$scope.serverDeletes = {values: deletes.results, key: 'Terminate', color: '#EF1818'}
//
//							$scope.serverData = function() {
//								$('.loading').hide();
//								return [$scope.serverCreates, $scope.serverDeletes]
//							}
//						});
//				});
//		}

	}])
	.controller('ResourcesServer', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
		$http({method: 'GET', url: '/api/resources/server/'+$routeParams.server_id}).
			success(function(data, status, headers, config) {
				$scope.server_id = $routeParams.server_id;
				$scope.server_data = data;
			});
	}])
	.controller('Servers', ['$scope', '$http', function($scope, $http) {

	}])
	.controller('Jobs', ['$scope', '$http', function($scope, $http) {
		$scope.pages = 0;
		$scope.page = 1;

		$scope.loadData = function () {
      $http({method: 'GET', url: '/api/jobs?page=' + $scope.page}).
          success(function(data, status, headers, config) {
              $scope.jobs = data.results;
							$scope.pages = data.total_pages;
          });
		};

		$scope.loadData();

		$scope.nextPage = function() {
			if ($scope.page <= $scope.pages)
			{
				$scope.page++;
				$scope.loadData();
			}
		};

		$scope.previousPage = function() {
			if ($scope.page > 0)
			{
				$scope.page--;
				$scope.loadData();
			}
		};
	}])
	;

function HeaderController($scope, $location)
{
    $scope.isActive = function (viewLocation) {
        return viewLocation === $location.path();
    };
}
