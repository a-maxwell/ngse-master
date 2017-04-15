app.factory('formService', function($http, $cookies, $location, authService) {
    var methods = {};

    var form = undefined;
    var categories = undefined;

    methods.fetchForm = function(callback) {
        return $http.get('/v1/forms')
        .then(function successCallback(response) {
            var d = response.data;
            for (var i = 0; i < d.length; i++) {
                if (d[i].status === "ongoing" && d[i].user === authService.getLevel()) {
                    form = d[i];
                    console.log(form);
                    break;
                }
            }

            $http.get('/v1/forms/categories', {params: {'form_id': form.id}})
            .then(function successCallback (response) {
                var d = response.data;
                categories = d;
                callback(d);
            }, function errorCallback(response) {
                callback(false);
            })
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.getForm = function() {
        return form;
    }

    methods.getCategories = function() {
        return categories;
    }

    methods.getCategory = function(id) {
        for (var i = 0; i < categories.length; i++) {
            if (categories[i].id == id) return categories[i];
        }
    }

    methods.fetchQuestions = function(callback, category_id) {
        return $http.get('/v1/forms/categories/questions', {params: {'category_id': category_id}})
        .then(function successCallback(response) {
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.fetchAnswers = function(callback, user_id, category_id) {
        return $http.get('/v1/users/answers', {params: {'user_id': user_id, 'category_id': category_id}})
        .then(function successCallback(response) {
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    return methods;
});