app.controller('navController', function($rootScope, $scope, $cookies, $location, $http, userService, authService, formService, messageService) {
	$scope.form = undefined;
	$scope.categories = undefined;

    $scope.debug = function() {
        console.log(userService.getUser());
        console.log(userService.answered());
    }

    $scope.loggedIn = authService.isLoggedIn;

	$scope.getLevel = authService.getLevel;

    $scope.logout = logout;

    function logout() {
    	authService.logout();
        messageService.pushMessage({
            text: 'Successfully logged out',
            type: 'info'
        });
    }
});