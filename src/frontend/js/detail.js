app.controller("detail", function($scope, $http, $rootScope, $routeParams) {

    var url = $rootScope.API_URL + "product/" + $routeParams.detailId;

    $http.get(url).then(function (response) {
        $scope.product = response.data;
        console.log(response.data);
    });

    $scope.backToList = function(){
    	location.href = "#/"+$routeParams.back;
    }

});