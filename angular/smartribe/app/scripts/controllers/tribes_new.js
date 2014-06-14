'use strict';

app.controller('TribesNewCtrl', function($location, $rootScope, $scope, Tribe){
  $scope.auth.promise.then(function(){
    if (!$rootScope.logged) {
      $location.path('/');
    }
    $scope.page.title = 'New tribe';
    $scope.tribeCreate = function(){
      Tribe.push($scope.tribe).success(function(data){
        $scope.alertLaunch('success', 'Successfully created tribe');
        $location.path('/tribes/' + data.tribeId);
      }).error(function(data){
        $scope.alertLaunch('error', data.detail);
      });
    };
  });
});
