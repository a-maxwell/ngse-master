app.controller('categoryManagerController', function($rootScope, $scope, $routeParams, adminService, authService) {

    initController();

    function initController() {
        $scope.loading = true;
        adminService.fetchCategories(function(c) {
        	$scope.categories = c;
            $scope.loading = false;
        });
    };
});