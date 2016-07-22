app.controller("menu", function($scope, $http, $rootScope, $window) {

    $scope.title = 'PONUKOVA_KARTA';

    $scope.backToList = function(){
    	location.href = "#/";
    }

    getGroups($rootScope.API_URL);

    $scope.background = function(url) {
        return {"background": "-moz-linear-gradient(top, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 59%, rgba(0, 0, 0, 0.65) 90%), url("+url+") no-repeat",
  "background": "-webkit-gradient(linear, left top, left bottom, color-stop(0%, rgba(0, 0, 0, 0)), color-stop(59%, rgba(0, 0, 0, 0)), color-stop(90%, rgba(0, 0, 0, 0.65))), url("+url+") no-repeat", "background": "-webkit-linear-gradient(top, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 59%, rgba(0, 0, 0, 0.65) 90%, url("+url+") no-repeat", "background": "-o-linear-gradient(top, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 59%, rgba(0, 0, 0, 0.65) 90%), url("+url+") no-repeat", "background": "-ms-linear-gradient(top, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 59%, rgba(0, 0, 0, 0.65) 90%), url("+url+") no-repeat",  "background": "linear-gradient(to bottom, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 59%, rgba(0, 0, 0, 0.65) 90%), url("+url+") no-repeat",  "background-position": "center", "background-size": "cover"};
    }

    function getGroups(base_url){

        var url = base_url + 'groups/'
        $http.get(url).then(function (response) {
            $scope.groups = response.data;
        });
    }

});
