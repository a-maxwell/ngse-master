app.factory('authService', function($rootScope, $http, $cookies, $location) {
    methods = {};

    function getExpiryDate() {
        var d = new Date();
        d.setHours(d.getHours() + 2);
        return d;
    }

    function setToken(token) {
        $cookies.put('token', token, {'expires': getExpiryDate()});
        $http.defaults.headers.common.Authorization = 'Bearer ' + token;
        if ($rootScope.debug) console.log($http.defaults.headers.common.Authorization);
    }

    function onRefresh() {
        var token = $cookies.get('token');
        if (token === undefined) return;
        $http.defaults.headers.common.Authorization = 'Bearer ' + token;
    }

    function sendData(url, data, callback) {
        return $http.post(url, data)
        .then(function successCallback(response) {
            var d = response.data;
            if ($rootScope.debug) console.log(d);
            if (d.success) setToken(d.token)
            callback(d);
        }, function errorCallback(response) {
            callback(false);
        });
    }

    methods.isLoggedIn = function() {
        return (!($cookies.get('token') === undefined));
    }

    methods.getUserID = function() {
        var token = $cookies.get('token');
        if (token === undefined) return 0;
        else return jwt_decode(token).sub;        
    }

    methods.getLevel = function() {
        token = $cookies.get('token');
        if (token === undefined) return 0;
        else return jwt_decode(token).level;
    }

    methods.verify = function(callback) {
        var token = $cookies.get('token');
        if (token === undefined) callback(false);
        else sendData('/v1/users/verify', {'token': token}, callback);
    }

    methods.authorize = function(level=10) {
        var token = $cookies.get('token');
        return (token === undefined) ? false : (jwt_decode(token).level <= level);
    }

    methods.register = function(data, callback) {
        if (data.scholarship) data.level = 5;
        else data.level = 4;
        delete data.scholarship;
        sendData('/v1/users/create', data, callback);
    }

    methods.login = function(data, callback) {
        sendData('/v1/users/login', data, callback);
    }

    methods.logout = function() {
        if ($rootScope.debug) console.log('removing token from cookies...');
        $cookies.remove('token');
        $http.defaults.headers.common.Authorization = '';
        if ($location.path() != '/auth') $location.path('/auth');
    }

    onRefresh();

    return methods;
});