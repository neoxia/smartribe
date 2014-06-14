'use strict';

app.factory('User', function($http, API_URL){
  return {
    push: function(user){
      return $http.post(API_URL + 'users/', user);
    },
    get: function(id){
      return $http.get(API_URL + 'users/' + id + '/');
    },
    getCurrent: function(){
      return $http.get(API_URL + 'users/');
    },
    edit: function(id, user){
      return $http.put(API_URL + 'users/' + id + '/', user);
    }
  };
});
