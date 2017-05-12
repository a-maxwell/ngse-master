app.factory('messageService', function($rootScope, $timeout, $location) {
    methods = {};

    var messages = [];
    var counter = 0;

    methods.getMessages = function() {
        return messages;
    }

    methods.pullMessage = function(id) {
        var index = -1;
        for (var i = 0; i < messages.length; i++) {
            if (messages[i].id == id) {
                index = i;
                break;
            }
        }
        $('#message-' + id).transition('fade');
        $timeout(function() {
            if (index > -1) messages.splice(index, 1);
        }, 100);
    }

    methods.pushMessage = function(obj) {
        obj.id = counter;
        counter = counter+1;
        messages.push(obj);
        $timeout(function() {
            methods.pullMessage(obj.id);
        }, 3000);
    }

    return methods;
});