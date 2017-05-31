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
app.directive('smRadioGroup', smRadioGroup).directive('smRadioButton', smRadioButton);
app.directive('select', function() {
  return {
    restrict: 'E', 
    link: function(scope, element) {
      setTimeout(function() {
        $(element).dropdown();
      }, 0)
    }
  }
});

function smRadioGroup() {
  return {
    restrict: 'E',
    replace: true,
    require: ['smRadioGroup', '?ngModel'],
    transclude: true,
    controller: smRadioGroupController,
    link: function(scope, element, attrs, ctrls) {
      var smRadioGroupCtrl = ctrls[0];
      var ngModelCtrl = ctrls[1];

      if (!ngModelCtrl) { return; }

      smRadioGroupCtrl.setNgModelCtrl(ngModelCtrl);
    },
    template: '<div class="ui buttons" ng-transclude></div>'
  };

  function smRadioGroupController() {
    /*jshint validthis: true */
    this._radioBtnElements = [];
    this._radioBtnFns = [];

    this.setNgModelCtrl = function(ngModelCtrl) {
      this._ngModelCtrl = ngModelCtrl;
      this._ngModelCtrl.$render = angular.bind(this, this.render);
    };

    this.registerBtnElement = function(element) {
      this._radioBtnElements.push(element);
    };

    this.addBtn = function(renderFn) {
      this._radioBtnFns.push(renderFn);
    };

    this.removeBtn = function(renderFn) {
      var btnIndex = this._radioBtnFns.indexOf(renderFn);
      if (btnIndex !== -1) {
        this._radioBtnFns.splice(btnIndex, 1);
      }
    };

    this.render = function() {
      this._radioBtnFns.forEach(function(renderFn) {
        renderFn();
      });
    };

    this.setViewValue = function(value, event) {
      this._ngModelCtrl.$setViewValue(value, event);
      this.render();
    };

    this.getViewValue = function() {
      return this._ngModelCtrl.$viewValue;
    };

  }
}

  function smRadioButton($animate) {
    return {
      restrict: 'E',
      replace: true,
      require: '^smRadioGroup',
      transclude: true,
      link: function(scope, element, attrs, smRadioGroupCtrl) {
        var isChecked;

        smRadioGroupCtrl.registerBtnElement(element);
        smRadioGroupCtrl.addBtn(render);
        attrs.$observe('value', render);

        element
          .on('click', eventListener)
          .on('$destroy', function() {
            smRadioGroupCtrl.removeBtn(render);
          });

        function eventListener(event) {
          if (element[0].hasAttribute('disabled') || attrs.value === void 0) { return; }

          scope.$apply(function() {
            smRadioGroupCtrl.setViewValue(attrs.value, event && event.type);
          });
        }

        function render() {
          var checked = (scope.$eval(attrs.value) === smRadioGroupCtrl.getViewValue());

          if(isChecked === checked) { return; }

          isChecked = checked;

          if(checked) {
            $animate.addClass(element, 'active');
          } else {
            $animate.removeClass(element, 'active');
          }
        }
      },
      template:'<div class="ui button" ng-transclude></div>'
    };
  }


app.config(function($routeProvider) {

    var _user = ["$q", "authService", function($q, authService) {
        if (!authService.authorize(10)) return $q.reject({"authorized": false});
    }];

    var _loggedIn = ["$q", "authService", function($q, authService) {
        if (authService.isLoggedIn()) return $q.reject({"authorized": true});
    }]

    var _decided = ["$q", "userService", function($q, userService) {
        if (!userService.answered()) return $q.reject({"answered": false});
    }]

    $routeProvider
    .when("/", {
        templateUrl: "/templates/home.html",
        resolve: {auth: _user}
    })
    .when("/admin", {
        templateUrl: "/templates/admin.html",
        resolve: {auth: _user}
    })
    .when("/admin/applicants", {
        templateUrl: "/templates/admin-applicants.html",
        resolve: {auth: _user}
    })
    .when("/admin/categories", {
        templateUrl: "/templates/admin-categories.html",
        resolve: {auth: _user}
    })
    .when("/application", {
        templateUrl: "/templates/application.html",
        controller: "summaryController",
        resolve: {auth: _user}
    })
    .when("/recommendation", {
        templateUrl: "/templates/recommendation.html",
        controller: "summaryController",
        resolve: {auth: _user}
    })
    .when("/recommendation/:id", {
        templateUrl: "/templates/form-recommender.html",
        controller: "formController",
        resolve: {auth: _user}
    })
    .when("/application/category", {
        templateUrl: "/templates/category.html",
        resolve: {auth: _user, answered: _decided}
    })
    .when("/application/:id", {
        templateUrl: "/templates/form.html",
        controller: "formController",
        resolve: {auth: _user, answered: _decided}
    })
    .when("/auth", {
        templateUrl: "/templates/lounge.html",
        resolve: {auth: _loggedIn,}
    })
    .when("/study", {
        templateUrl: "/templates/study.html",
        resolve: {auth: _user}
    })
    .otherwise({redirectTo: '/'});
});


app.run(["$rootScope", "$location", function($rootScope, $location) {
    $rootScope.debug = true;

    $rootScope.$on("$routeChangeError", function(event, current, previous, eventObj) {
      if (eventObj.authorized === false) $location.path('/auth');
      if (eventObj.answered === false) $location.path('/study');
    });
}]);