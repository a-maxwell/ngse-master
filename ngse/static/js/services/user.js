app.factory('userService', function($rootScope, $http, $cookies, $location, authService) {
    var methods = {};

    var user = {};

    methods.userAnswered = function() {
        return (user != {});
    }

    methods.fetchUser = function(callback) {
        var user_id = authService.getUserID();
        return $http.get('/v1/users/show', {params: {'user_id': user_id}})
        .then(function successCallback(response) {
            var d = response.data;
            user = d;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.getUser = function() {
        return user;
    }

    methods.saveAnswers = function(callback, user_controller) {
        var user_id = authService.getUserID();

        $http.post('/v1/users/update', {'user_id': user_id, 'user': user_controller})
        .then(function successCallback(response) {
            user = user_controller;
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    return methods;
});