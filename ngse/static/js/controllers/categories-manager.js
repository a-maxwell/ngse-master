app.controller('applicantManagerController', function($rootScope, $scope, $routeParams, adminService, authService) {

    initController();

    function initController() {
        $scope.loading = true;
        adminService.fetchApplicants(function(a) {
        	$scope.applicants = a;
            $scope.loading = false;
        });
    };
});