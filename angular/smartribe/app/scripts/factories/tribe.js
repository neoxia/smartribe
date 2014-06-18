'use strict';

app.factory('Tribe', function($http, API_URL){
  return {
    edit: function(id, tribe){
      return $http.put(API_URL + 'tribes/' + id + '/', tribe);
    },
    get: function(id){
      return $http.get(API_URL + 'tribes/' + id + '/');
    },
    getAll: function(){
      return $http.get(API_URL + 'tribes/');
    },
    push: function(tribe){
      return $http.post(API_URL + 'tribes/', tribe);
    }
  };
});
