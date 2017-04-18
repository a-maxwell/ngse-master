app.controller('navController', function($rootScope, $scope, $cookies, $location, $http, authService, formService) {
	$scope.form = undefined;
	$scope.categories = undefined;

    $scope.debug = function() {
        formService.fetchAnswers(function(d) {
            console.log(d);
        }, authService.getUserID(), 1);
    }

    $scope.loggedIn = authService.isLoggedIn;

    $scope.logout = authService.logout;
});