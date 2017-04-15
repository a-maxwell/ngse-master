app.controller('formController', function($rootScope, $scope, $routeParams, formService, authService) {

    $scope.id = $routeParams.id;

	$scope.category = formService.getCategory($scope.id);

	initController();

    function initController() {
        $scope.loading = true;
        formService.fetchQuestions(function(e) {
        	if ($rootScope.debug) console.log(e);
        	formService.fetchAnswers(function(a) {
        		if ($rootScope.debug) console.log(a);

        		for (var i = 0; i < e.length; i++) {
        			if (e[i].class != 'question') continue;

        			for (var j = 0; j < a.length; j++) {
        				if (a[j].question_id != e[i].id) continue;

    					e[i].answer = a[j];
    					a.splice(j, 1);
    					break;
        			}
        		}

	        	$scope.elements = e;
	        	$scope.loading = false;
        		if ($rootScope.debug) console.log($scope.elements);

        	}, authService.getUserID(), $scope.id);
        }, $scope.id);
    };
});