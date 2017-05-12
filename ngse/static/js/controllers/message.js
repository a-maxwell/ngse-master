app.controller('messageController', function($rootScope, $scope, $timeout, messageService) {

    $scope.messages = messageService.getMessages;

    $scope.close = messageService.pullMessage;
    // $scope.load = messageService.pushMessage;
    $scope.load = load;

    function load(obj) {
        messageService.pushMessage(obj);
    }

	initController();

    function initController() {
        $scope.load({
            text: 'Welcome to NGSE!',
            type: 'info'
        });
    };
});