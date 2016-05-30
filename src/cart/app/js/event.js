app.controller("event", function($scope, $http, $rootScope) {
    $scope.title = "Event cart";

    var url = $rootScope.API_URL + "product/event/list/";
    
    $http.get(url).then(function (response) {
        $scope.products = response.data;
    });

    $scope.showDetail = function(id){
    	location.href = "#/detail/"+id;
    }
    
});