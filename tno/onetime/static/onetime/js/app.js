'use strict';

var TrustNoOneApp = angular.module('TrustNoOneApp', [
  'ngResource',
  'ngRoute'
])
  .config([
    '$locationProvider',
    '$routeProvider',
    function ($locationProvider,
              $routeProvider) {

      $routeProvider
        .when('/new/', {
          templateUrl: '/message-create.html',
          controller : 'MessageCreateController'
        })
        .when('/thanks/', {
          templateUrl: '/message-created.html',
          controller : 'MessageCreatedController'
        })
        .when('/faq/', {
          templateUrl: '/faq.html'
        })
        .otherwise('/faq/');

      $locationProvider.html5Mode(true);
    }])
  .config([
    '$interpolateProvider',
    '$httpProvider',
    '$resourceProvider',
    function ($interpolateProvider,
              $httpProvider,
              $resourceProvider) {
      // $interpolateProvider.startSymbol('[[');
      // $interpolateProvider.endSymbol(']]');

      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';

      $resourceProvider.defaults.stripTrailingSlashes = false;
    }
  ]);
