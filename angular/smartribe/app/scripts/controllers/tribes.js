'use strict';

app.controller('TribesCtrl', function($location, $rootScope, $scope, Tribe){
  $scope.auth.promise.then(function(){
    if (!$rootScope.logged) {
      $location.path('/');
    }
    $scope.page.title = 'Tribes list';
    Tribe.getAll().success(function(data){
      $scope.tribes = data;
    }).error(function(data){
      $scope.tribes = [];
      $scope.alertLaunch('error', data.detail);
    });
  });
});
