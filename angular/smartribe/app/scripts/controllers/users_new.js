'use strict';

app.controller('UsersNewCtrl', function($location, $rootScope, $scope, User){
  $scope.auth.promise.then(function(){
    if ($rootScope.logged) {
      $location.path('/');
    }
    $scope.page.title = 'Signup';
    $scope.page.activeNav = 'signup';
    $scope.signup = function(){
      $scope.errors = undefined;
      User.push($scope.user).success(function(){
        $scope.alertLaunch('success', 'Successfully signed up');
        $location.path('/');
      }).error(function(data){
        $scope.errors = data;
        $scope.alertLaunch('error', 'Error while signing up');
      });
    };
  });
});
