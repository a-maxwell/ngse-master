app.controller('navController', function($rootScope, $scope, $cookies, $location, $http, authService, formService) {
	$scope.form = undefined;
	$scope.categories = undefined;

    $scope.debug = function() {
        formService.fetchForm(function(d) {
            var level = authService.getLevel()
            for (var i = 0; i < d.length; i++) {
                if (d[i].status === "ongoing" && d[i].user === level) {
                    $scope.form = d[i];
                }
            }
            formService.fetchCategories(function(d) {
                $scope.categories = d;
            }, $scope.form.id);
        });
    }

    $scope.loggedIn = authService.isLoggedIn;

    $scope.logout = authService.logout;
});