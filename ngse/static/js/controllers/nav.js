app.controller('navController', function($scope, $cookies, $location, authService) {

    $scope.debug = function() {
        console.log($scope.loggedIn());
    }

    $scope.loggedIn = authService.isLoggedIn;

    $scope.logout = authService.logout;
});