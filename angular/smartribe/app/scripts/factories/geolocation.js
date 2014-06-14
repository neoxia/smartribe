'use strict';

app.factory('Geolocation', function($q, $rootScope, $window){
  return {
    get: function(){
      var deferred = $q.defer();
      if ($window.navigator && $window.navigator.geolocation) {
        $window.navigator.geolocation.getCurrentPosition(function(position){
          deferred.resolve(position);
        }, function(error){
          switch (error.code) {
            case 1:
              deferred.reject('You have rejected access to your location');
              break;
            case 2:
              deferred.reject('Unable to determine your location');
              break;
            case 3:
              deferred.reject('Service timeout has been reached');
              break;
          }
        });
      } else {
        deferred.reject('Browser does not support location services');
      }
      return deferred.promise;
    }
  };
});
