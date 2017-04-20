app.factory('adminService', function($rootScope, $http, $cookies, $location) {
    methods = {};

    function postData(url, data, callback) {
        return $http.post(url, data)
        .then(function successCallback(response) {
            var d = response.data;
            if ($rootScope.debug) console.log(d);
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    function getData(url, data, callback) {
        return $http.get(url, {params: data})
        .then(function successCallback(response) {
            var d = response.data;
            if ($rootScope.debug) console.log(d);
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.fetchForms = function(callback) {
        getData('/v1/users', undefined, callback);
    }

    methods.fetchCategories = function(callback) {
        var forms = [];
        methods.fetchForms(function(f) {
            for (var i = 0; i < f.length; i++) {
                if (f[i].status == "ongoing") forms.push(f[i]);
            }
        })

        var categories = [];

        for (var i = 0; i < forms.length; i++) {
            var c = [];
            getData('/v1/forms/categories', {'form_id': forms[i].id}, function(cats) {
                for (var j = 0; j < cats.length; j++) {
                    break;
                }
            })
        }
    }

    methods.fetchApplicants = function(callback) {
        getData('/v1/users', undefined, function(users) {
            var applicants = [];
            for (var i = 0; i < users.length; i++) {
                if (users[i].user_type == "Non-ERDT Applicant" || users[i].user_type == "ERDT Applicant") applicants.push(users[i]);
            }
            callback(applicants);
        })
    }

    return methods;
});