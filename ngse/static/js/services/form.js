app.factory('formService', function($rootScope, $http, $cookies, $location, authService, userService) {
    var methods = {};

    var form = undefined;
    var categories = undefined;

    methods.fetchForm = function(callback) {
        return $http.get('/v1/forms')
        .then(function successCallback(response) {
            var d = response.data;
            console.log(d);
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

    methods.submitForm = function(callback) {
        return $http.post('/v1/users/update', {'submitted': true})
        .then(function successCallback(response) {
            userService.fetchUser(function(data) {
                console.log(data);
            });
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback({success: false});
        });
    }

    methods.getCategories = function() {
        return categories;
    }

    methods.getCategory = function(id) {
        for (var i = 0; i < categories.length; i++) {
            if (categories[i].id == id) return categories[i];
        }
    }

    methods.fetchElements = function(callback, category_id) {
        return $http.get('/v1/forms/categories/elements', {params: {'category_id': category_id}})
        .then(function successCallback(response) {
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.fetchAnswers = function(callback, user_id, category_id) {
        return $http.get('/v1/users/answers/show', {params: {'user_id': user_id, 'category_id': category_id}})
        .then(function successCallback(response) {
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.saveAnswers = function(callback, user_id, answers, category_id) {

        data = [];
        for (var i = 0; i < answers.length; i++) {
            data.push({
                'id': answers[i].id,
                'text': answers[i].text
            });
        }

        $http.post('/v1/users/answers/update', {'user_id': user_id, 'category_id': category_id, 'data': data, 'length': data.length})
        .then(function successCallback(response) {
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.clear = function() {
        form = undefined;
        categories = undefined;
    }

    methods.debug = function() {
        return $http.get('/v1/users')
        .then(function successCallback(response) {
            var d = response.data;
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        })
    }

    return methods;
});