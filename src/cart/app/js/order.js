app.controller("order", function($scope, $http, $rootScope) {
   
   	$scope.count = 0;
	$scope.computeItem = function() {
		$scope.count += $scope.item;
	};
	
	$scope.sendOrder = function() {
		window.alert("Sended order");
	};

	$scope.calculateDiscount = function(){
		$scope.discount = $scope.count / 2;
	}
	$scope.$watch('item', $scope.calculateDiscount);
	
	
});