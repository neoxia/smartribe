'use strict';

app.factory('Token', function($cookieStore){
  return {
    get: function(){
      return $cookieStore.get('smartribeToken');
    },
    set: function(token){
      $cookieStore.put('smartribeToken', token);
    },
    destroy: function(){
      $cookieStore.remove('smartribeToken');
    }
  };
});
