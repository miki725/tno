'use strict';

angular.module('TrustNoOneApp')
  .controller('MessageCreateController', [
    '$scope',
    'OTSecretService',
    'TNOCrypto',
    'TNOState',
    '$log',
    '$location',
    function ($scope,
              OTSecretService,
              TNOCrypto,
              TNOState,
              $log,
              $location) {

      $scope.encrypting = false;
      $scope.message = {
        'password': 'HelloWorld1',
        'message' : 'hello world'
      };
      $scope.uuid = null;

      $scope.are_we_there_yet = function () {
        return angular.isDefined($scope.message.message)
               && $scope.message.message !== ''
               && angular.isDefined($scope.message.password)
               && $scope.message.password !== ''
               && !$scope.encrypting;
      };

      $scope.create_message = function () {
        if (!$scope.are_we_there_yet()) {
          return;
        }

        $scope.encrypting = true;
        TNOCrypto.get_entropy()
          .then(function (entropy) {
            var crypto = TNOCrypto.encode(TNOCrypto.encrypt(
              entropy,
              $scope.message.password,
              $scope.message.message
            ));
            return OTSecretService.save(crypto);
          })
          .then(function (data) {
            TNOState.state.created = data;
          })
          .finally(function () {
            $scope.message.message = undefined;
            $scope.message.password = undefined;
            $scope.encrypting = false;
            $location.path('/thanks/');
          });
      };
    }
  ]);
