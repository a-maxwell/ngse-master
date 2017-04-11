app.controller('formController', function($scope, $cookies, $location, formService) {

	$scope.categories = [];

	initController();

    $scope.debug = function() {
        console.log($scope.categories);
    }

    function initController() {
        $scope.loading = true;

    };
});