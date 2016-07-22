app.controller("menu", function($scope, $http, $rootScope) {

    $scope.title = 'PONUKOVA_KARTA';

    $scope.backToList = function(){
    	location.href = "#/";
    }

    getGroups($rootScope.API_URL);


    function getGroups(base_url){

        var url = base_url + 'groups/'
        $http.get(url).then(function (response) {
            $scope.groups = response.data;
            console.log($scope.groups);
        });
    }

});
