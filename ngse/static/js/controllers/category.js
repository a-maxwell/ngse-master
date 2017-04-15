app.controller('categoryController', function($rootScope, $scope, formService, authService) {
    $scope.loading = true;

	initController();

    $scope.debug = function() {
        console.log($scope.categories);
    }

    function initController() {
        formService.fetchForm(function(d) {
            $scope.categories = formService.getCategories();
        	$scope.loading = false;
        });
    };
});