'use strict';

angular.module('TrustNoOneApp')
  .factory('OTSecretService', [
    '$resource',
    function ($resource) {
      return $resource('/api/v1/one-time-secrets/:uuid/', {'id': '@uuid'});
    }
  ]);
