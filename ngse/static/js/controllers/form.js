app.controller('formController', function($rootScope, $scope, $routeParams, $location, formService, authService, userService, messageService) {

    $scope.id = $routeParams.id;
	$scope.category = formService.getCategory($scope.id);

    initController();
    
    $scope.save = save;
    $scope.back = back;

    function back() {
        var data = $location.path().split('/', 3);
        var location = '/' + data[1];
        $location.path(location);
    }

    function save() {
        $scope.loading = true;
        answers = [];

        console.log('initialized save()')

        for (var i = 0; i < $scope.elements.length; i++) {
            var e = $scope.elements[i]
            if (e.klass != 'question') continue;
            var a = e.answer;
            if (a.text === "") {
                if (e.required) {
                    if (e.kind === "date") continue;
                    console.log(e);
                    // messageService.pushMessage({
                    //     text: "A required field is missing",
                    //     type: "error"
                    // });
                    $scope.loading = false;
                    return false;
                }
            }
            answers.push(a);
        }

        formService.saveAnswers(function(d) {
            if ($rootScope.debug) console.log(d);
            userService.fetchUser(function(data) {
                console.log(data);
            })
            messageService.pushMessage({
                text: $scope.category.name + ' saved',
                type: 'info'
            });
            back();
        }, authService.getUserID(), answers, $scope.id);
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

                setTimeout(function() {
                    // $(".ui.dropdown").dropdown();
                    $(".ui.calendar").calendar({
                        type: "date"
                    }); 
                }, 0);

        	}, authService.getUserID(), $scope.id);
        }, $scope.id);
    };
});