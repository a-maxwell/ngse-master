var app = angular.module("NGSEApp", ["ngRoute", "ngCookies"], function($httpProvider) {
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

    /**
    * The workhorse; converts an object to x-www-form-urlencoded serialization.
    * @param {Object} obj
    * @return {String}
    */ 
    var param = function(obj) {
        var query = '', name, value, fullSubName, subName, subValue, innerObj, i;

        for(name in obj) {
            value = obj[name];

            if(value instanceof Array) {
                for(i=0; i<value.length; ++i) {
                    subValue = value[i];
                    fullSubName = name + '[' + i + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += param(innerObj) + '&';
                }
            }
            else if(value instanceof Object) {
                for(subName in value) {
                    subValue = value[subName];
                    fullSubName = name + '[' + subName + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += param(innerObj) + '&';
                }
            }
            else if(value !== undefined && value !== null)
            query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
        }

        return query.length ? query.substr(0, query.length - 1) : query;
    };

    // Override $http service's default transformRequest
    $httpProvider.defaults.transformRequest = [function(data) {
        return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
    }];
});

app.factory('AuthenticationService', function($http, $cookies, $location) {
    methods = {};

    function getExpiryDate() {
        var d = new Date();
        d.setHours(d.getHours() + 1);
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

app.controller('headerController', function($scope, $cookies, $location, AuthenticationService) {

    $scope.debug = function() {
        console.log($scope.loggedIn());
    }

    $scope.loggedIn = AuthenticationService.isLoggedIn;

    $scope.logout = AuthenticationService.logout;
});

app.controller('authController', function($scope, $location, AuthenticationService) {

    initController();

    $scope.signin = signin;
    $scope.register = register;

    function signin() {
        // alert('submitting a login form!');
        $scope.login.loading = true;
        AuthenticationService.login($scope.login.email, $scope.login.password, function(data) {
            if (data.success === true) $location.path('/');
            else {
                $scope.login.message = data.message;
                $scope.login.loading = false;
            }
        });

    };

    function register() {
        // alert('submitting a registration form!');
        $scope.registration.loading = true;
        AuthenticationService.register($scope.registration.last, $scope.registration.given, $scope.registration.middlemaiden, $scope.registration.email, function(data) {
            if (data['success'] === true) $location.path('/');
            else {
                $scope.registration.message = data['message'];
                $scope.registration.loading = false;
            }
        });

    };

    function initController() {
        AuthenticationService.verify(function(valid) {
            console.log('Token Validity: ' + valid);
            if (!valid) AuthenticationService.logout()
            else $location.path('/');
        });
    };
});

app.config(function($routeProvider) {

    var _user = ["$q", "AuthenticationService", function($q, AuthenticationService) {
        if (!AuthenticationService.authorize(10)) return $q.reject({"authorized": false});
    }];

    var _loggedIn = ["$q", "AuthenticationService", function($q, AuthenticationService) {
        if (AuthenticationService.isLoggedIn()) return $q.reject({"authorized": true});
    }]

    $routeProvider
    .when("/", {
        templateUrl: "/templates/home.html",
        resolve: {auth: _auth}
    })
    .when("/application", {
        templateUrl: "/templates/application.html",
        resolve: {auth: _auth}
    })
    // .when("/about", {
    //     templateUrl: "/templates/about.html",
    //     resolve: res
    // })
    // .when("/documents", {
    //     templateUrl: "/templates/documents.html",
    //     resolve: res
    // })
    // .when("/contact", {
    //     templateUrl: "/templates/contact.html",
    //     resolve: res
    // })
    .when("/auth", {
        templateUrl: "/templates/lounge.html",
        resolve: {auth: _loggedIn}
    })
    .otherwise({redirectTo: '/'});
});

app.run(["$rootScope", "$location", function($rootScope, $location) {

    $rootScope.$on("$routeChangeError", function(event, current, previous, eventObj) {
        if (eventObj.authorized === false) $location.path('/auth');
        else $location.path('/')
    });
}]);