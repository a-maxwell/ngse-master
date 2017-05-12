app.controller('summaryController', function($rootScope, $scope, $routeParams, $location, authService, userService, formService) {

    function initController() {

        if ($scope.user() === {}) {
            userService.fetchUser(function(data) {
                console.log(data);
            })
        }

        if ($scope.categories === undefined) {
            formService.fetchForm(function(data) {
                console.log(data);
                $scope.categories = data;
            })
        }
    };

    $scope.user = userService.getUser;
    $scope.categories = formService.getCategories();

    initController();

    $scope.debug = debug;
    $scope.status = status;

    $scope.allAnswered = allAnswered;

    $scope.application_status = application_status;
    $scope.validation_status = validation_status;

    $scope.convertToID = convertToID;

    function convertToID(str) {
        return str.toLowerCase().replace(" ", "-");
    }

    function validation_status() {
        return $scope.user().validation_status;
    }

    function application_status() {
        return $scope.user().application_status;
    }

    function allAnswered() {
        if (!$scope.user().answered_pos) return false;
        for (var i = 0; i < $scope.user().answered.length; i++) {
            if (!$scope.user().answered[i].status) return false;
        }
        return true;
    }

    function status(category_id) {
        for (var i = 0; i < $scope.user().answered.length; i++) {
            if ($scope.user().answered[i].category_id == category_id) return ($scope.user().answered[i].status) ? "Answered" : "Unanswered";
        }
    }

    function debug() {
        console.log($scope.user());
        console.log($scope.categories);
    }

});