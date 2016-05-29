app.controller("detail", function($scope, $http, $rootScope, $routeParams) {

    var url = $rootScope.API_URL + "product/" + $routeParams.detailId;

    $http.get(url).then(function (response) {
    	console.log(response.data);
        $scope.product = response.data[0];
    });

});