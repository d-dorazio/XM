$(document).ready(function(){
   $('.parallax').parallax();
 });



 angular.module('xmclient', [])
 .controller('xmController', ['$scope', '$http',
   function($scope, $http) {

     function maybeAddAsync(url) {
       return url + "?async=" + $scope.async;
     }

     $scope.async = false;
     $scope.forward = function () {
       console.log("forward called");
       console.log($scope.async);
       $http.get(maybeAddAsync("http://192.168.0.1/api/forward")).
       success(function(data, status, headers, config) {
    // this callback will be called asynchronously
    // when the response is available
    }).
    error(function(data, status, headers, config) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  })};
  $scope.backward = function () {
    console.log("backward called");
    console.log($scope.async);
    $http.get(maybeAddAsync("http://192.168.0.1/api/backward")).
    success(function(data, status, headers, config) {
 // this callback will be called asynchronously
 // when the response is available
 }).
 error(function(data, status, headers, config) {
 // called asynchronously if an error occurs
 // or server returns response with an error status.
})};
$scope.left = function () {
  console.log("left called");
  console.log($scope.async);
  $http.get(maybeAddAsync("http://192.168.0.1/api/left")).
  success(function(data, status, headers, config) {
// this callback will be called asynchronously
// when the response is available
}).
error(function(data, status, headers, config) {
// called asynchronously if an error occurs
// or server returns response with an error status.
})};
$scope.right = function () {
  console.log("right called");
  console.log($scope.async);
  $http.get(maybeAddAsync("http://192.168.0.1/api/right")).
  success(function(data, status, headers, config) {
// this callback will be called asynchronously
// when the response is available
}).
error(function(data, status, headers, config) {
// called asynchronously if an error occurs
// or server returns response with an error status.
})};
$scope.stop = function () {
if($scope.async){
    console.log("stop called");
    console.log($scope.async);
  $http.get("http://192.168.0.1/api/stop").
  success(function(data, status, headers, config) {
// this callback will be called asynchronously
// when the response is available
}).
error(function(data, status, headers, config) {
// called asynchronously if an error occurs
// or server returns response with an error status.
})}};

}]);
