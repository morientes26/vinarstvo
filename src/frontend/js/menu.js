app.controller("menu", function($scope, $http, $rootScope, $routeParams) {

    $scope.title = 'PONUKOVA_KARTA';

    $scope.backToList = function(){
    	location.href = "#/";
    }

});
