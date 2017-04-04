angular.module('Login', []);
angular.module('Authentication')
.controller('LoginController',
	['$scope', '$rootScope', '$location', 'AuthenticationService',
	function ($scope, $rootScope, $location, AuthenticationService) {
		// reset login status
		AuthenticationService.ClearCredentials();
		$scope.login = function () {
			$scope.dataLoading = true;
			AuthenticationService.Login($scope.username, $scope.password, function(response) {
				if(response.success) {
					AuthenticationService.SetCredentials($scope.username, $scope.password);
					$location.path('/');
				} else {
					$scope.error = response.message;
					$scope.dataLoading = false;
				}
			});
		};
	}]
);




angular.module("NGSEApp", ["ngRoute", "ngCookies"])
.config(function($routeProvider) {
	$routeProvider
	.when("/", {
		templateUrl: "/templates/home.html"
	})
	.when("/news", {
		templateUrl: "/templates/news.html"
	})
	.when("/about", {
		templateUrl: "/templates/about.html"
	})
	.when("/documents", {
		templateUrl: "/templates/documents.html"
	})
	.when("/contact", {
		templateUrl: "/templates/contact.html"
	})
	.when("/lounge", {
		templateUrl: "/templates/lounge.html"
	})
	
	.otherwise({ redirectTo: '/' });
});
// .controller('NGSEController', ['$scope', '$cookies', '$cookieStore', '$window', function($scope, $cookies, $cookieStore, $window) {

// }]);