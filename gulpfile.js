var gulp = require('gulp');
var sass = require('gulp-sass');
var coffee = require('gulp-coffee');

gulp.task('hello', function(){
	console.log('Hello Gulp.js');
});

gulp.task('coffee', function() {
  gulp.src('./js/**/*.coffee')
    .pipe(coffee({bare: true}))
    .pipe(gulp.dest('./javascripts/'));
});

gulp.task('coffee:watch', function () {
	gulp.watch('./js/**/*.coffee', ['coffee']);
});


gulp.task('sass', function () {
  return gulp.src('./css/*.sass')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./css/'));
});

gulp.task('sass:watch', function () {
  gulp.watch('./css/*.sass', ['sass']);
});

gulp.task('default', ['sass:watch', 'coffee:watch',"sass","coffee"]);
