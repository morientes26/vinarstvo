app.controller("list", function($scope, $http, $rootScope) {
    $scope.title = "Wine cart";

    var url = $rootScope.API_URL + "product/list/";
    
    $http.get(url).then(function (response) {
        $scope.products = response.data;
    });

    $scope.showDetail = function(id){
    	location.href = "#/detail/"+id;
    }

});