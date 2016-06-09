app.controller("list", function($scope, $http, $rootScope, $cookies, $routeParams, shoppingcart) {
    
    $scope.title = "Vinna karta";
    $scope.isOrder = false;
    $scope.items = shoppingcart.getCustomer().items;

    var url = $rootScope.API_URL + "product/list/";
    $scope.event = 2; // default event for product list
    if ($routeParams.page=="event"){
    	url = $rootScope.API_URL +"product/event/list/";
    	$scope.title = "Vinna karta ochutnavky";
    }
    
    $http.get(url).then(function (response) {
        $scope.products = response.data;
    });

    $scope.showDetail = function(id){
    	location.href = "#/detail/"+id;
    }
    $scope.addToCart = function(id, name){
    	shoppingcart.add(id,name);
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.removeFromCart = function(id){
    	shoppingcart.remove(id);
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.cleanOrder = function(){
    	shoppingcart.clear();
    	$scope.isOrder = false;
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.showOrder = function(){
    	$scope.shoppinglist = shoppingcart.getJsonItems();
    	$scope.sum_price = 0;
    	for ($item in $scope.shoppinglist){
			$scope.sum_price += $scope.shoppinglist[$item].amount;
    	}    	
    	$scope.isOrder = true;
    }
    $scope.sendOrder = function(form) {    	

    	if (form.$valid){
    		var url = $rootScope.API_URL + "order/create/";

			var dataObj = {
				customer_name : shoppingcart.getCustomer().name,  //form.customer_name.$viewValue
				contact_detail: form.contact_detail.$viewValue,
				email: form.email.$viewValue,
				phone: form.phone.$viewValue,
				event : form.event.$viewValue,
				items : shoppingcart.getJsonItems()
			};	
			console.log(dataObj);
			var res = $http.post(url, dataObj);
			res.success(function(data, status, headers, config) {
				$scope.message = 'Objednavka bola odoslana';
				$scope.cleanOrder();
			});
			res.error(function(data, status, headers, config) {
				console.log( "failure message: " + JSON.stringify({data: data}));
				$scope.message = 'Pri odosielani objednavky vznikla chyba';
			});		
		} else {
			console.log('not valid form');
		}
	};
});