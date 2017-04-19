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

app.config(function($routeProvider) {

    var _user = ["$q", "authService", function($q, authService) {
        if (!authService.authorize(10)) return $q.reject({"authorized": false});
    }];

    var _loggedIn = ["$q", "authService", function($q, authService) {
        if (authService.isLoggedIn()) return $q.reject({"authorized": true});
    }]

    $routeProvider
    .when("/", {
        templateUrl: "/templates/home.html",
        resolve: {auth: _user}
    })
    .when("/application", {
        templateUrl: "/templates/application.html",
        resolve: {auth: _user}
    })
    .when("/recommendation", {
        templateUrl: "/templates/category.html",
        resolve: {auth: _user}
    })
    .when("/recommendation/:id", {
        templateUrl: "/templates/application.html",
        controller: "formController",
        resolve: {auth: _user}
    })
    .when("/application/category", {
        templateUrl: "/templates/category.html",
        resolve: {auth: _user}
    })
    .when("/application/category/:id", {
        templateUrl: "/templates/form.html",
        controller: "formController",
        resolve: {auth: _user}
    })
    .when("/auth", {
        templateUrl: "/templates/lounge.html",
        resolve: {auth: _loggedIn,}
    })
    .otherwise({redirectTo: '/'});
});

app.run(["$rootScope", "$location", function($rootScope, $location) {
    $rootScope.debug = true;

    $rootScope.$on("$routeChangeError", function(event, current, previous, eventObj) {
        if (eventObj.authorized === false) $location.path('/auth');
        else $location.path('/')
    });
}]);