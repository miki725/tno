'use strict';

var TrustNoOneApp = angular.module('TrustNoOneApp', [
  'ngResource',
  'ui.router'
])
  .config([
    '$locationProvider',
    '$stateProvider',
    '$urlRouterProvider',
    function ($locationProvider,
              $stateProvider,
              $urlRouterProvider) {

      $urlRouterProvider.otherwise('/new/');

      $stateProvider
        .state('new', {
          url        : '/new/',
          templateUrl: '/message-create.html',
          controller : 'MessageCreateController'
        })
        .state('created', {
          url        : '/thanks/',
          templateUrl: '/message-created.html',
          controller : 'MessageCreatedController'
        })
        .state('view', {
          url        : '/read/{uuid:[a-f0-9]{32}}/',
          templateUrl: '/message.html',
          controller : 'MessageController'
        })
        .state('faq', {
          url        : '/faq/',
          templateUrl: '/faq.html'
        });

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
