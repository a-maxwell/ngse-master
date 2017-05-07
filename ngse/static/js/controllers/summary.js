app.controller('summaryController', function($rootScope, $scope, $routeParams, $location, authService, userService) {

    function initController() {
        $scope.user = userService.getUser();

        if ($scope.user === {}) {
            userService.fetchUser(function(data) {
                console.log(data);
                $scope.user = data;
            })
        }
    };

    initController();

    $scope.debug = debug;

    function debug() {
        console.log($scope.user);
    }

});