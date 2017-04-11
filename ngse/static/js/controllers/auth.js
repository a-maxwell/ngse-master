app.controller('authController', function($scope, $location, authService) {

    initController();

    $scope.signin = signin;
    $scope.register = register;

    function signin() {
        // alert('submitting a login form!');
        $scope.login.loading = true;
        authService.login($scope.login.email, $scope.login.password, function(data) {
            if (data.success === true) {
                if (authService.authorize(1)) $location.path('/admin');
                if (authService.authorize(3)) $location.path('/application');
                else $location.path('/recommendation');
            }
            else {
                $scope.login.message = data.message;
                $scope.login.loading = false;
            }
        });

    };

    function register() {
        // alert('submitting a registration form!');
        $scope.registration.loading = true;
        authService.register($scope.registration.last, $scope.registration.given, $scope.registration.middlemaiden, $scope.registration.email, function(data) {
            if (data['success'] === true) $location.path('/');
            else {
                $scope.registration.message = data['message'];
                $scope.registration.loading = false;
            }
        });

    };

    function initController() {
        authService.verify(function(valid) {
            console.log('Token Validity: ' + valid);
            if (!valid) authService.logout()
            else $location.path('/');
        });
    };
});