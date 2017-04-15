app.controller('authController', function($rootScope, $scope, $location, authService) {

    initController();

    $scope.signin = signin;
    $scope.register = register;

    function signin() {
        if ($rootScope.debug) console.log('submitting a login form!');
        l = $scope.login;
        l.loading = true;
        data = {'email': l.email, 'password': l.password}
        authService.login(data, function(data) {
            if (data.success === true) {
                if (authService.authorize(1)) $location.path('/admin');
                if (authService.authorize(4) ||  authService.authorize(5)) $location.path('/application');
                else $location.path('/recommendation');
            }
            else l.message = data.message;
            l.loading = false;
        });

    };

    function register() {
        if ($rootScope.debug) console.log('submitting a registration form!');
        r = $scope.registration;
        r.loading = true;
        data = {'last': r.last, 'given': r.given, 'middlemaiden': r.middlemaiden, 'email': r.email, 'scholarship': r.scholarship}
        authService.register(data, function(data) {
            if (data['success'] === true) $location.path('/');
            else r.message = data.message;
            r.loading = false;
        });

    };

    function initController() {
        authService.verify(function(d) {
            if (d === false) validity = false;
            else validity = d.success;

            if ($rootScope.debug) console.log('Token Validity: ' + validity);
            if (!validity) authService.logout()
            else $location.path('/');
        });
    };
});