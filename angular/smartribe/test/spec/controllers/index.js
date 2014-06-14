'use strict';

describe('Controller: IndexCtrl', function(){
  var IndexCtrl, scope;
  beforeEach(module('smartribeApp'));
  beforeEach(inject(function($controller, $rootScope){
    scope = $rootScope.$new();
    IndexCtrl = $controller('IndexCtrl', {
      $scope: scope
    });
  }));
  it('should work', function(){
    //expect(scope.test).toBe(true);
  });
});
