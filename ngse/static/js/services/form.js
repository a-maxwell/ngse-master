app.factory('formService', function($http, $cookies, $location, authService) {
    methods = {};

    name = '';

    categories = [];

    function fetchForm(callback) {
        return $http.post('/v1/forms')
        .then(function successCallback(response) {
            var d = response.data;
            
        }, function errorCallback(response) {
            callback(false);
        });
    }

    function fetchCategories(response) {
        return $http.post('/v1/forms/categories', {'token': token})
        .then(function successCallback(response) {
            var d = response.data;
            callback(d.success);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    return methods;
});