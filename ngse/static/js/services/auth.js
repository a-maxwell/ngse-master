app.factory('authService', function($http, $cookies, $location) {
    methods = {};

    function getExpiryDate() {
        var d = new Date();
        d.setHours(d.getHours() + 2);
        return d;
    }

    function setToken(token) {
        $cookies.put('token', token, {'expires': getExpiryDate()});
        $http.defaults.headers.common.Authorization = 'Bearer ' + token;
    }

    methods.isLoggedIn = function() {
        return (!($cookies.get('token') === undefined));
    }

    methods.verify = function(callback) {
        var token = $cookies.get('token');
        if (token === undefined) callback(false);
        return $http.post('/v1/users/verify', {'token': token})
        .then(function successCallback(response) {
            var d = response.data;
            callback(d.success);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.authorize = function(level=10) {
        var token = $cookies.get('token');
        return (token === undefined) ? false : (jwt_decode(token)['level'] <= level);
    }

    methods.register = function(last, given, middlemaiden, email, callback) {
        return $http.post('/v1/users/create', {'last': last, 'given': given, 'middlemaiden': middlemaiden, 'email': email})
        .then(function(response) {
            var d = response.data;
            console.log(d);
            if (d.success) setToken(d.token);
            callback(d);
        });
    }

    methods.login = function(email, password, callback) {
        return $http.post('/v1/users/login', {'email': email, 'password': password})
        .then(function(response) {
            var d = response.data;
            console.log(d);
            if (d.success) setToken(d.token);
            callback(d);
        });
    }

    methods.logout = function() {
        console.log('removing token from cookies...');
        $cookies.remove('token');
        $http.defaults.headers.common.Authorization = '';
        $location.path('/auth');
    }

    return methods;
});