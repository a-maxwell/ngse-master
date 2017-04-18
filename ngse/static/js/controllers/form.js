app.controller('formController', function($rootScope, $scope, $routeParams, formService, authService) {

    $scope.id = $routeParams.id;
	$scope.category = formService.getCategory($scope.id);

    initController();
    
    $scope.save = save;

    function save() {
        answers = [];

        for (var i = 0; i < $scope.elements.length; i++) {
            if ($scope.elements[i].klass != 'question') continue;
            answers.push($scope.elements[i].answer);
        }

        formService.saveAnswers(function(d) {
            if ($rootScope.debug) console.log(d);
        }, authService.getUserID(), answers);
    }

    function initController() {
        $scope.loading = true;
        formService.fetchElements(function(e) {
        	formService.fetchAnswers(function(a) {
        		for (var i = 0; i < e.length; i++) {
        			if (e[i].klass != 'question') continue;

        			for (var j = 0; j < a.length; j++) {
        				if (a[j].element_id != e[i].id) continue;

    					e[i].answer = a[j];
                        delete e[i].answer.last_modified;
                        delete e[i].answer.date_created;
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