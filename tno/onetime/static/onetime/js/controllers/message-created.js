'use strict';

angular.module('TrustNoOneApp')
  .controller('MessageCreatedController', [
    '$scope',
    '$location',
    'TNOState',
    '$state',
    '$log',
    '$timeout',
    function ($scope,
              $location,
              TNOState,
              $state,
              $log,
              $timeout) {
      angular.extend($scope, TNOState.get());

      $scope.get_message_link = function () {
        if (angular.isDefined($scope.created)
            && angular.isDefined($scope.created.uuid)) {
          return HOST_URL + $state.href('view', {'uuid': $scope.created.uuid});
        } else {
          return '';
        }
      };

      if (!angular.isDefined($scope.created)) {
        $location.path('/new/');
      }
    }
  ]);
