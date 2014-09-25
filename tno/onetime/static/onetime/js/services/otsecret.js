'use strict';

angular.module('TrustNoOneApp')
  .factory('OTSecretService', [
    '$resource',
    function ($resource) {
      return $resource('/api/v1/one-time-secret/:uuid/', {'id': '@uuid'});
    }
  ]);
