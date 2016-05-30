app.controller("list", function($scope, $http, $rootScope, $cookies, shoppingcart) {
    
    $scope.title = "Wine cart";
    $scope.items = shoppingcart.getCustomer().items;

    var url = $rootScope.API_URL + "product/list/";
    
    $http.get(url).then(function (response) {
        $scope.products = response.data;
    });

    $scope.showDetail = function(id){
    	location.href = "#/detail/"+id;
    }
    $scope.addToCart = function(id){
    	shoppingcart.add(id);
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.removeFromCart = function(id){
    	shoppingcart.remove(id);
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.cleanOrder = function(){
    	shoppingcart.clear();
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.sendOrder = function() {
		window.alert("Sended order");
	};
});