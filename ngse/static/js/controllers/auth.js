app.controller('authController', function($rootScope, $scope, $location, authService, userService) {

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
                userService.fetchUser(function(d) {
                    console.log(d);
                })
                if (authService.getLevel() === 1 || authService.getLevel() === 2) $location.path('/admin');
                else if (authService.getLevel() === 3) $location.path('/recommendation');
                else $location.path('/');
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
            if (data['success'] === true) {
                userService.fetchUser(function(d) {
                    console.log(d);
                })
                $location.path('/');
            }
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